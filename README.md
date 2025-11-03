<p align="center">
  <img src="interface/assets/images/DEX-banner-LD-1.png" alt="cpp-tbox logo"/>
</p>

# 🧠 DEX – Digitally Excellent Xhell (AI Dataset Collection)

Welcome to the **DEX Universal AI Dataset**, the official data foundation for the **DEX Shell Project** — an AI-driven, multi-modal command shell that understands **sign language**, **gestures**, **voice**, and **contextual intent**.

This dataset series enables the development and research of **multi-sensory human-computer interaction**, featuring components for machine learning, gesture recognition, and contextual reasoning.
(DEX-OFF-SOFTWARE-DEVELOPMENT\DEX-Shell\assets\images\DEX-banner.png)
---

## 📂 Dataset Overview

### 1️⃣ `dex_sign_language.csv`
Maps physical hand signs and symbolic gestures to DEX commands.  
Used for **sign-language recognition** and gesture–command translation.

**Columns**
| Column | Description |
|--------|-------------|
| `sign_id` | Unique ID for each gesture/sign |
| `gesture_name` | Gesture label or name |
| `dex_command` | Mapped shell command |
| `meaning` | Semantic description of the sign |
| `complexity_level` | Difficulty or motion complexity (1–5) |

---

### 2️⃣ `dex_gesture_telemetry.csv`
Captures **frame-by-frame 3D hand motion data** simulating live gesture telemetry.  
Used for **gesture tracking**, **motion prediction**, and **AI hand modeling**.

**Columns**
| Column | Description |
|--------|-------------|
| `frame` | Frame index in the gesture sequence |
| `x_l, y_l, z_l` | Left-hand 3D position |
| `x_r, y_r, z_r` | Right-hand 3D position |
| `speed` | Relative movement speed |
| `angle` | Angle of motion between frames |
| `command_label` | Associated DEX command or gesture name |

---

### 3️⃣ `dex_command_usage.csv`
Tracks DEX user activity and execution performance for analytics and reinforcement learning.

**Columns**
| Column | Description |
|--------|-------------|
| `timestamp` | UTC time of execution |
| `user_id` | Unique anonymized user ID |
| `command` | Executed DEX command |
| `context` | Task context or environment |
| `duration_ms` | Execution duration (milliseconds) |
| `result` | Outcome (success / error / timeout) |

---

### 4️⃣ `dex_ai_reasoning_logs.json`
Synthetic dataset showing DEX’s **AI interpretation reasoning** — how it maps uncertain input to decisions.

**Sample Format**
```json
{
  "input": "gesture unclear",
  "interpreted": "dex stop process",
  "confidence": 0.78
}

