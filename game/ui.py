import tkinter as tk
from tkinter import messagebox, simpledialog

from .engine import GameEngine
from .utils import load_high_scores, save_high_scores
from .constants import COLORS


class WordleGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Word Guess")
        self.root.geometry("940x780")
        self.root.resizable(True, True)
        self.root.minsize(720, 650)

        self.engine = GameEngine()
        self.high_scores = load_high_scores()

        # Game state
        self.username = ""
        self.current_level = 1
        self.high_level = 0
        self.hard_mode = False
        self.secret_word = ""
        self.attempts_left = 6
        self.current_row = 0
        self.current_col = 0
        self.letter_states = {}
        self.alpha_labels = {}

        self.get_username()
        self.setup_ui()
        self.new_game()

    def get_username(self):
        while not self.username:
            self.username = simpledialog.askstring(
                "Welcome", "Enter your username:", parent=self.root
            )
            if not self.username:
                if messagebox.askyesno("Exit", "You must enter a username to play. Exit?"):
                    self.root.destroy()
                    exit()
                continue

            self.username = self.username.strip()
            if len(self.username) < 3:
                messagebox.showwarning("Invalid", "Username must be at least 3 characters.")
                self.username = ""
                continue

        self.high_score = self.high_scores.get(self.username, 0)

    def setup_ui(self):
        # Scrollable Canvas
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Mouse wheel support
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        # Main container
        main_frame = tk.Frame(self.scrollable_frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.columnconfigure(1, weight=0)

        # ================= LEFT HALF - GAME BOARD =================
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        tk.Label(left_frame, text="GAME BOARD", font=("Helvetica", 18, "bold")).pack(pady=10)

        self.grid_frame = tk.Frame(left_frame)
        self.grid_frame.pack(pady=15)

        for i in range(6):
            self.grid_frame.rowconfigure(i, weight=1)
        for i in range(5):
            self.grid_frame.columnconfigure(i, weight=1)

        self.cells = [[None] * 5 for _ in range(6)]
        for r in range(6):
            for c in range(5):
                lbl = tk.Label(
                    self.grid_frame,
                    text="",
                    font=("Helvetica", 28, "bold"),
                    relief="ridge",
                    bd=4,
                    bg="#ffffff",
                    width=3,
                    height=2
                )
                lbl.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
                self.cells[r][c] = lbl

        # ================= VERTICAL SEPARATOR =================
        separator = tk.Frame(main_frame, width=3, bg="#888888")
        separator.grid(row=0, column=1, sticky="ns", padx=10)

        # ================= RIGHT HALF - INFO + ALPHABET =================
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        tk.Label(right_frame, text="GAME INFO", font=("Helvetica", 18, "bold")).pack(pady=10)

        # Player Info
        self.user_label = tk.Label(
            right_frame, 
            text=f"Player: {self.username}", 
            font=("Helvetica", 13, "bold"), 
            fg="blue"
        )
        self.user_label.pack(pady=5)

        # Stats
        stats_frame = tk.Frame(right_frame)
        stats_frame.pack(pady=8, fill="x")
        self.level_label = tk.Label(stats_frame, text=f"Level: {self.current_level}", font=("Helvetica", 14))
        self.level_label.pack(pady=3)
        self.high_label = tk.Label(stats_frame, text=f"Best Level: {self.high_level}", font=("Helvetica", 12))
        self.high_label.pack(pady=3)

        # Hard Mode
        self.hard_var = tk.BooleanVar()
        tk.Checkbutton(
            right_frame, 
            text="Hard Mode (4 attempts)", 
            variable=self.hard_var,
            font=("Helvetica", 11), 
            command=self.toggle_hard_mode
        ).pack(pady=12)

        # Alphabet Tracker
        tk.Label(right_frame, text="LETTER TRACKER", font=("Helvetica", 14, "bold")).pack(pady=(20, 5))
        
        alpha_container = tk.Frame(right_frame)
        alpha_container.pack(pady=8)

        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for keys in rows:
            row_frame = tk.Frame(alpha_container)
            row_frame.pack(pady=4)
            for letter in keys:
                lbl = tk.Label(
                    row_frame,
                    text=letter,
                    width=3,
                    height=2,
                    font=("Helvetica", 11, "bold"),
                    relief="ridge",
                    bd=2,
                    bg=COLORS['DEFAULT']
                )
                lbl.pack(side=tk.LEFT, padx=2)
                self.alpha_labels[letter] = lbl

        # Submit Button
        self.submit_btn = tk.Button(
            right_frame,
            text="SUBMIT WORD",
            font=("Helvetica", 14, "bold"),
            bg="#4a7c59",
            fg="white",
            width=18,
            height=3,
            command=self.submit_guess
        )
        self.submit_btn.pack(pady=30)

        # Bottom Controls
        btn_frame = tk.Frame(right_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="New Game", width=12, command=self.new_game).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Change User", width=12, command=self.change_user).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Quit", width=10, command=self.quit_game).pack(side=tk.LEFT, padx=5)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

    def toggle_hard_mode(self):
        self.hard_mode = self.hard_var.get()

    def handle_keypress(self, event):
        key = event.keysym.upper()

        if key.isalpha() and len(key) == 1 and self.current_col < 5:
            self.cells[self.current_row][self.current_col].config(text=key, bg="#ffffff", fg="black")
            self.current_col += 1

        elif key == "BACKSPACE" and self.current_col > 0:
            self.current_col -= 1
            self.cells[self.current_row][self.current_col].config(text="", bg="#ffffff")

        elif key in ("RETURN", "ENTER"):
            self.submit_guess()
            
    def flash_invalid(self):
        original_colors = [self.cells[self.current_row][c].cget("bg") for c in range(5)]
        for c in range(5):
            self.cells[self.current_row][c].config(bg="#ff6b6b")
        self.root.after(180, lambda: self.restore_row_colors(original_colors))

    def restore_row_colors(self, original_colors):
        for c in range(5):
            self.cells[self.current_row][c].config(bg=original_colors[c])

    def submit_guess(self):
        guess = "".join(self.cells[self.current_row][c].cget("text") for c in range(5))

        if len(guess) != 5:
            messagebox.showwarning("Incomplete", "Please enter all 5 letters.")
            return
        
        if not self.engine.is_valid_word(guess):
            self.flash_invalid()
            messagebox.showwarning("Invalid Word", f"'{guess}' is not a valid English word")
            return

        if guess == self.secret_word:
            self.handle_win(guess)
            return

        if self.attempts_left <= 1:
            self.game_over()
            return

        feedback = self.engine.get_feedback(guess, self.secret_word)
        self.update_grid(guess, feedback)
        self.update_alphabet_colors(guess, feedback)

        self.current_row += 1
        self.current_col = 0
        self.attempts_left -= 1

    def update_grid(self, guess, feedback):
        color_map = COLORS
        for i in range(5):
            self.cells[self.current_row][i].config(
                text=guess[i],
                bg=color_map[feedback[i]],
                fg="white"
            )

    def update_alphabet_colors(self, guess, feedback):
        color_map = COLORS
        for letter, fb in zip(guess, feedback):
            if letter in self.alpha_labels:
                current_state = self.letter_states.get(letter)
                if (fb == 'G' or 
                    (fb == 'Y' and current_state != 'G') or 
                    (fb == 'X' and current_state is None)):
                    self.alpha_labels[letter].config(bg=color_map[fb], fg="white")
                    self.letter_states[letter] = fb

    def handle_win(self, guess):
        for i in range(5):
            self.cells[self.current_row][i].config(text=guess[i], bg=COLORS['G'], fg="white")

        messagebox.showinfo(
            "Level Complete!",
            f"🎉 Well done {self.username}!\n"
            f"The word was {self.secret_word}\n"
        )

        self.current_level += 1
        self.new_level()

    def game_over(self):
        messagebox.showinfo("Game Over", f"The word was: {self.secret_word}")
        self.save_high_score_for_user()
        self.new_game()

    def new_level(self):
        self.secret_word = self.engine.get_random_word()
        self.attempts_left = 4 if self.hard_mode else 6
        self.current_row = 0
        self.current_col = 0
        self.letter_states.clear()

        # Clear grid
        for r in range(6):
            for c in range(5):
                self.cells[r][c].config(text="", bg="#ffffff", fg="black")

        # Reset alphabet
        for lbl in self.alpha_labels.values():
            lbl.config(bg=COLORS['DEFAULT'], fg="black")

        self.level_label.config(text=f"Level: {self.current_level}")

    def new_game(self):
        self.current_level = 1
        self.new_level()
        self.update_stats()

    def update_stats(self):
        self.level_label.config(text=f"Level: {self.current_level}")
        if self.current_level - 1 > self.high_score:
            self.high_level = self.current_level -1
            self.high_label.config(text=f"Best Level: {self.high_level}")

    def save_high_level(self):
        if self.current_level - 1 > self.high_scores.get(self.username, 0):
            self.high_scores[self.username] = self.current_level - 1
        save_high_scores(self.high_scores)

    def change_user(self):
        self.save_high_level()
        self.get_username()
        self.user_label.config(text=f"Player: {self.username}")
        self.high_level = self.high_scores.get(self.username, 0)
        self.high_label.config(text=f"Best: {self.high_score}")
        self.new_game()

    def quit_game(self):
        if messagebox.askyesno("Exit", "Save scores and quit?"):
            self.save_high_level()
            self.root.destroy()

    def run(self):
        self.root.bind("<Key>", self.handle_keypress)
        self.root.mainloop()