"""
gesture_engine.py

- Data loader for CSV dataset format
- Keras model (LSTM-based) for sequence classification
- Train / evaluate / inference utilities
- Integration hooks for motion tracker (ctypes or pybind11)

Requirements:
    pip install numpy pandas tensorflow opencv-python scikit-learn

"""
import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path
import json

# ML libs
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / 'training_dataset'
REF_DIR = HERE / 'gesture_reference'

# Optional: load C++ bindings if available
try:
    import motion_tracker_bindings as mtb
    HAVE_BINDINGS = True
except Exception:
    HAVE_BINDINGS = False


def load_csv_sequences(csv_path: Path, seq_len=16):
    """Load CSV where each line is a frame with flattened keypoints and a label.
    Groups by sequence_id and resamples/pads to `seq_len` frames per sequence.
    Returns: X (N, seq_len, kp*2), y (N,)
    """
    df = pd.read_csv(csv_path)
    groups = df.groupby('sequence_id')
    X = []
    y = []
    for sid, g in groups:
        frames = []
        for _, row in g.sort_values('frame_idx').iterrows():
            # extract all kp columns
            kp_cols = [c for c in df.columns if c.startswith('kp_')]
            vals = row[kp_cols].values.astype(np.float32)
            frames.append(vals)
        # pad/truncate
        if len(frames) >= seq_len:
            frames = frames[:seq_len]
        else:
            # pad by repeating last frame
            while len(frames) < seq_len:
                frames.append(frames[-1])
        X.append(np.stack(frames, axis=0))
        y.append(g['label'].iloc[0])
    X = np.array(X)
    y = np.array(y)
    return X, y


def build_model(input_shape, n_classes):
    # LSTM-based sequence classifier
    inp = layers.Input(shape=input_shape)
    x = layers.Masking(mask_value=0.0)(inp)
    x = layers.TimeDistributed(layers.Dense(128, activation='relu'))(x)
    x = layers.LSTM(128, return_sequences=False)(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(64, activation='relu')(x)
    out = layers.Dense(n_classes, activation='softmax')(x)
    model = models.Model(inputs=inp, outputs=out)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def train(csv_path: str, epochs=30, batch_size=32, seq_len=16, model_out='gesture_model.h5'):
    csv_path = Path(csv_path)
    X, y = load_csv_sequences(csv_path, seq_len=seq_len)
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    n_classes = len(le.classes_)
    print('Classes:', le.classes_)
    X_train, X_val, y_train, y_val = train_test_split(X, y_enc, test_size=0.15, random_state=42)

    model = build_model(input_shape=X.shape[1:], n_classes=n_classes)
    model.summary()

    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size)
    model.save(model_out)

    # save label encoder
    with open('label_encoder.json', 'w') as f:
        json.dump({'classes': le.classes_.tolist()}, f)
    print('Saved model ->', model_out)


class GestureEngine:
    def __init__(self, model_path='gesture_model.h5', label_json='label_encoder.json'):
        if not Path(model_path).exists():
            raise FileNotFoundError('Model not found, run train() first')
        self.model = tf.keras.models.load_model(model_path)
        with open(label_json, 'r') as f:
            data = json.load(f)
            self.classes = data['classes']

    def predict_from_sequence(self, seq: np.ndarray):
        # seq shape: (seq_len, kp*2)
        if seq.ndim == 2:
            seq = np.expand_dims(seq, 0)
        probs = self.model.predict(seq)
        idx = np.argmax(probs, axis=-1)[0]
        return self.classes[idx], float(np.max(probs))

    def capture_and_predict(self, cam_index=0, seq_len=16):
        # capture seq_len frames via C++ bindings or OpenCV fallback
        frames = []
        if HAVE_BINDINGS:
            for _ in range(seq_len):
                try:
                    vals = mtb.capture_landmarks(cam_index)
                except Exception as e:
                    print('Binding capture error:', e)
                    break
                # vals is a flat list [x0,y0,x1,y1...]
                arr = np.array(vals, dtype=np.float32)
                frames.append(arr)
        else:
            import cv2
            cap = cv2.VideoCapture(cam_index)
            if not cap.isOpened():
                raise RuntimeError('Camera not available')
            for _ in range(seq_len):
                ret, frame = cap.read()
                if not ret:
                    break
                # naive skin-detection landmarks via OpenCV (placeholder)
                # Here we simply resize and flatten grayscale values as a quick fallback
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                small = cv2.resize(gray, (21, 21))
                arr = small.flatten().astype(np.float32) / 255.0
                frames.append(arr)
            cap.release()

        if len(frames) < seq_len:
            raise RuntimeError('Failed to capture enough frames')

        seq = np.stack(frames, axis=0)
        # if raw image fallback used, adjust shape to model expectation
        if seq.shape[1] != self.model.input_shape[-1]:
            # attempt simple projection/padding/truncate
            target = self.model.input_shape[-1]
            seq2 = np.zeros((seq_len, target), dtype=np.float32)
            for i in range(seq_len):
                a = seq[i]
                if a.size >= target:
                    seq2[i] = a[:target]
                else:
                    seq2[i, :a.size] = a
            seq = seq2

        return self.predict_from_sequence(seq)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', type=str, help='CSV path to train on')
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--model-out', type=str, default='gesture_model.h5')
    args = parser.parse_args()

    if args.train:
        train(args.train, epochs=args.epochs, model_out=args.model_out)
    else:
        print('No action specified. Use --train to train a model.')