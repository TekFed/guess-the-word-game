import random
from .constants import load_words

class GameEngine:
    def __init__(self):
        self.word_list, self.word_set = load_words()

    def get_random_word(self):
        return random.choice(self.word_list)
    
    def is_valid_word(self, guess):
        if not guess or len(guess) != 5:
            return False
        return guess.upper() in self.word_set

    def get_feedback(self, guess, secret):
        feedback = ['X'] * 5
        secret_count = {}

        # Green pass
        for i in range(5):
            if guess[i] == secret[i]:
                feedback[i] = 'G'
            else:
                secret_count[secret[i]] = secret_count.get(secret[i], 0) + 1

        # Yellow pass
        for i in range(5):
            if feedback[i] == 'X' and guess[i] in secret_count and secret_count[guess[i]] > 0:
                feedback[i] = 'Y'
                secret_count[guess[i]] -= 1

        return feedback