# Word Guess Game 🎮

A modern, feature-rich **Wordle-style** word guessing game built with Python and Tkinter.

![Game Preview](https://github.com/TekFed/guess-the-word-game/blob/master/docs/screenshot-01.png)  


## ✨ Features

- **Physical keyboard input** (type directly, Backspace & Enter supported)
- **Smart Alphabet Tracker** – letters change color (Green/Yellow/Gray) just like the grid
- **Username system** with individual high score tracking
- **Hard Mode** (4 attempts instead of 6)
- **Multiple levels** with progressive scoring
- **Persistent high scores** saved in JSON

## 🎯 How to Play

1. Enter your username when prompted
2. Type any 5-letter word using your keyboard
3. Press **Enter** or click **SUBMIT WORD**
4. Interpret the colors:
   - 🟩 **Green** = Correct letter in correct position
   - 🟨 **Yellow** = Correct letter in wrong position
   - ⬜ **Gray** = Letter not in the word
5. Try to guess the word in as few attempts as possible
6. Complete levels to increase your score

## 🚀 Installation & Running

### Prerequisites
- Python 3.8 or higher

### Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/word-guess-game.git

# Navigate to project folder
cd word-guess-game

# Run the game
python main.py
```

## 📁 Project Structure

```plaintext
word-guess-game/
├── main.py                 # Entry point
├── README.md
├── highscores.json         # Auto-generated
├── game/
│   ├── __init__.py
│   ├── constants.py        # Colors and word loading
│   ├── engine.py           # Game logic (feedback, random word)
│   ├── ui.py               # Tkinter GUI + interface
│   └── utils.py            # Save/Load high scores
└── assets/
    └── words.txt           # Expandable word list
```

## 🎨 Controls

| Action              | Method                  |
|---------------------|-------------------------|
| Type letters        | Physical keyboard       |
| Delete letter       | Backspace               |
| Submit guess        | Enter key or Submit button |
| Scroll window       | Mouse wheel / Scrollbar |

## 🛠️ Customization

- Add more words in `assets/words.txt` (one word per line)
- Modify scoring logic in `game/ui.py`
- Change colors in `game/constants.py`
- Adjust window size or layout easily

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new features
- Improve UI/UX
- Fix bugs
- Expand the word list

1. Fork the project
2. Create your feature branch
3. Submit a Pull Request

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

**Made with ❤️, Grok, and lots of ☕**

---
