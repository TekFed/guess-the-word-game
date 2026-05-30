import json
import os

def load_high_scores():
    try:
        if os.path.exists("highscores.json"):
            with open("highscores.json", "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_high_scores(data):
    try:
        with open("highscores.json", "w") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass