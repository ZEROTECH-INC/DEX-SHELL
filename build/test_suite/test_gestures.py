def test_gesture_reference_loaded():
    import json
    data = json.load(open("sign_language/gesture_reference/dex_gestures.json"))
    assert "hand_open" in data