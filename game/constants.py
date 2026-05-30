import os

COLORS = {
    'G': "#6aaa64",   # Green
    'Y': "#c9b458",   # Yellow
    'X': "#787c7e",   # Gray
    'DEFAULT': "#d3d6da"
}

def load_words():
    words_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'words.txt')
    try:
        with open(words_path, 'r') as f:
            words = [word.strip().upper() for word in f if len(word.strip()) == 5]
            return words, set(words)
    except FileNotFoundError:
        fallback = [
            "APPLE", "BRAIN", "CRANE", "DREAM", "EAGLE", "FLAME", "GHOST", "HOUSE",
            "IMAGE", "JUICE", "KNIFE", "LEMON", "MAGIC", "NIGHT", "OCEAN", "PEACE",
            "QUEEN", "RIVER", "STONE", "TIGER", "UNITY", "VOICE", "WORLD", "YOUTH",
            "ZEBRA", "BEACH", "CATCH", "DANCE", "EARTH", "FAITH"
        ]
        return fallback, set(fallback)