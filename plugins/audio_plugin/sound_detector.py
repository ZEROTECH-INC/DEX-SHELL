#!/usr/bin/env python3
"""
plugins/audio_plugin/sound_detector.py

DEX Audio Plugin - Sound Detector
- Lightweight real-time audio monitor (prints JSON events)
- Uses sounddevice + numpy to read mic input and compute amplitude & dominant frequency
Note: For production, wrap prints into IPC/event emitter to core.
"""
import time
import json
from pathlib import Path

try:
    import numpy as np
    import sounddevice as sd
except Exception:
    np = None
    sd = None

PLUGIN_NAME = "dex.audio"
SAMPLE_RATE = 44100
CHUNK = 2048

class SoundDetector:
    def __init__(self, sample_rate=SAMPLE_RATE, chunk=CHUNK):
        self.sample_rate = sample_rate
        self.chunk = chunk
        self.stream = None

    def process_audio_block(self, block):
        if np is None:
            return None
        block = np.asarray(block).reshape(-1)
        amplitude = float(np.sqrt(np.mean(block.astype(float)**2)))
        freqs = np.fft.rfft(block)
        mags = np.abs(freqs)
        if mags.size == 0:
            dominant_freq = 0.0
        else:
            dom_idx = int(np.argmax(mags))
            dominant_freq = dom_idx * (self.sample_rate / self.chunk)
        return {"timestamp": time.time(), "amplitude": round(amplitude,6), "dominant_freq": round(dominant_freq,2)}

    def callback(self, indata, frames, time_info, status):
        try:
            block = indata[:, 0]
            info = self.process_audio_block(block)
            if info:
                print(json.dumps(info), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)

    def start(self):
        if sd is None:
            raise RuntimeError("sounddevice not available. Install dependency.")
        self.stream = sd.InputStream(channels=1, samplerate=self.sample_rate, blocksize=self.chunk, callback=self.callback)
        self.stream.start()
        print(f"[{PLUGIN_NAME}] Listening (sr={self.sample_rate})")

    def stop(self):
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
        print(f"[{PLUGIN_NAME}] Stopped.")

if __name__ == "__main__":
    det = SoundDetector()
    try:
        det.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        det.stop()