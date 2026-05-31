import os

COLORS = {
    'G': "#6aaa64",   # Green
    'Y': "#c9b458",   # Yellow
    'X': "#787c7e",   # Gray
    'DEFAULT': "#d3d6da"
}


def load_words():
    """Load words and return both list and set for fast validation"""
    words_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'words.txt')
    
    try:
        with open(words_path, 'r', encoding='utf-8') as f:
            words = []
            for line in f:
                word = line.strip().upper()
                if len(word) == 5 and word.isalpha():
                    words.append(word)
            
            if not words:
                raise ValueError("No valid words found")
                
            return words, set(words)   # list for random choice, set for fast lookup
            
    except FileNotFoundError:
        print(f"Warning: words.txt not found at {words_path}. Using fallback words.")
        fallback = ["APPLE", "BRAIN", "CRANE", "DREAM", "EAGLE", "FLAME", "GHOST", "HOUSE", "IMAGE", "JUICE"]
        return fallback, set(fallback)
    except Exception as e:
        print(f"Error loading words: {e}")
        fallback = ["APPLE", "BRAIN", "CRANE", "DREAM", "EAGLE"]
        return fallback, set(fallback)