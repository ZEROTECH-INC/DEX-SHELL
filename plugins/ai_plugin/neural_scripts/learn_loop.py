#!/usr/bin/env python3
# plugins/ai_plugin/neural_scripts/learn_loop.py
import time, random
print("[ai_plugin] Starting mock learn loop")
for epoch in range(1,6):
    loss = random.random() * 0.5
    print(f"epoch={epoch} loss={loss:.4f}")
    time.sleep(0.2)
print("[ai_plugin] Done")