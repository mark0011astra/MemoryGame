import tkinter as tk
import random
import time
from collections import deque


class WorkingMemoryTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Working Memory Booster")

        # --- 設定 ---
        self.grid_size = 3
        self.initial_display_time = 800  # やや長めに設定
        self.flash_duration = 300
        self.correct_flash_color = "sea green"
        self.incorrect_flash_color = "salmon"
        self.start_round = 2  # 少し複雑な状態から開始
        self.n_back_level = 2  # Dual N-Back の N

        # --- 状態変数 ---
        self.buttons = []
        self.active_sequence = []
        self.user_sequence = []
        self.score = 0
        self.high_score = 0
        self.game_active = False
        self.display_time = self.initial_display_time
        self.last_highlighted = None
        self.current_round = 0
        self.start_time = 0
        self.reaction_times = []
        self.n_back_history = deque(maxlen=self.n_back_level)

        # --- GUI要素 ---
        self._setup_ui()

    def _setup_ui(self):
        # スコアフレーム
        self.score_frame = tk.Frame(self.root, bg="white")
        self.score_frame.grid(row=0, column=0, columnspan=self.grid_size, sticky="ew")
        self.score_label = tk.Label(self.score_frame, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.pack(pady=10)
        self.high_score_label = tk.Label(self.score_frame, text=f"High Score: {self.high_score}", font=("Helvetica", 16))
        self.high_score_label.pack(pady=10)

        # ボタンの作成
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                button = tk.Button(self.root, bg="dark gray", width=8, height=4,
                                   command=lambda x=i, y=j: self.user_click(x, y))
                button.grid(row=i + 1, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

        # コントロールパネル
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=self.grid_size + 1, column=0, columnspan=self.grid_size, pady=10)

        self.start_button = tk.Button(control_frame, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(control_frame, text="Reset", command=self.reset_game, state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.time_label = tk.Label(control_frame, text=f"Display Time: {self.display_time / 1000:.2f}s")
        self.time_label.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="+", command=lambda: self.adjust_time(100)).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="-", command=lambda: self.adjust_time(-100)).pack(side=tk.LEFT, padx=2)

        # N-Back レベル調整
        n_back_frame = tk.Frame(self.root)
        n_back_frame.grid(row=self.grid_size + 2, column=0, columnspan=self.grid_size, pady=5)
        tk.Label(n_back_frame, text="N-Back Level:").pack(side=tk.LEFT)
        tk.Button(n_back_frame, text="-", command=self._decrease_n_back).pack(side=tk.LEFT)
        self.n_back_label = tk.Label(n_back_frame, text=str(self.n_back_level))
        self.n_back_label.pack(side=tk.LEFT)
        tk.Button(n_back_frame, text="+", command=self._increase_n_back).pack(side=tk.LEFT)

        # フィードバックラベル
        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.feedback_label.grid(row=self.grid_size + 3, column=0, columnspan=self.grid_size)

    # --- 心理学的アプローチ ---
    def _apply_chunking(self, sequence):
        # 長いシーケンスを3-4要素のチャンクに分割 (例)
        chunk_size = random.randint(3, 4)
        for i in range(0, len(sequence), chunk_size):
            yield sequence[i:i + chunk_size]

    # --- マスの操作 ---
    def highlight_cell(self, x, y):
        self.buttons[x][y].config(bg="light sky blue") # 視覚的な区別を明確に

    def reset_cell_color(self):
        for row in self.buttons:
            for button in row:
                button.config(bg="dark gray")

    def get_random_cell(self):
        while True:
            cell = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if cell != self.last_highlighted:
                self.last_highlighted = cell
                return cell

    # --- ユーザーインタラクション ---
    def user_click(self, x, y):
        if not self.game_active:
            return

        timestamp = time.time()
        self.reaction_times.append(timestamp - self.start_time)

        self.user_sequence.append((x, y))

        # Dual N-Back のチェック
        if len(self.active_sequence) > self.n_back_level:
            if self.user_sequence[-1] == self.active_sequence[-self.n_back_level]:
                print("N-Back match!") # フィードバック

        if self.user_sequence[-1] != self.active_sequence[len(self.user_sequence) - 1]:
            self.update_score(success=False)
            self.feedback_label.config(text="Incorrect!", fg="red")
            self.game_over()
        elif len(self.user_sequence) == len(self.active_sequence):
            self.check_sequence()

    # --- シーケンスのチェック ---
    def check_sequence(self):
        self.score = self.current_round  # スコアを現在のラウンド数に
        self.update_score(success=True)
        self.feedback_label.config(text="Correct!", fg="green")
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")
        self.root.after(1000, self.new_round)

    # --- スコアの更新 ---
    def update_score(self, success):
        if success:
            self.score_frame.config(bg=self.correct_flash_color)
            self.root.after(self.flash_duration, lambda: self.score_frame.config(bg="white"))
            self.score_label.config(text=f"Score: {self.score}", fg="forest green")
        else:
            self.score_label.config(text=f"Score: {self.score}", fg="firebrick")
            self.score_frame.config(bg=self.incorrect_flash_color)
            self.root.after(self.flash_duration, lambda: self.score_frame.config(bg="white"))

    # --- ゲームフロー ---
    def start_game(self):
        self.score = 0
        self.current_round = self.start_round
        self.update_score(success=True)
        self.game_active = True
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.active_sequence = [self.get_random_cell() for _ in range(self.current_round)]
        self.show_sequence()

    def game_over(self):
        self.game_active = False
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.reset_cell_color()
        self.active_sequence = []
        self.user_sequence = []
        print("Game Over")
        # パフォーマンス分析 (例)
        if self.reaction_times:
            avg_reaction_time = sum(self.reaction_times) / len(self.reaction_times)
            print(f"Average reaction time: {avg_reaction_time:.3f} seconds")

    def reset_game(self):
        self.game_over()
        self.score = 0
        self.update_score(success=True)
        self.feedback_label.config(text="")

    def new_round(self):
        if not self.game_active:
            return
        self.user_sequence = []
        self.current_round += 1
        self.active_sequence.append(self.get_random_cell())
        self.show_sequence()

    def show_sequence(self):
        self.reset_cell_color()
        self.start_time = time.time() # ラウンド開始時刻を記録
        for i, cell in enumerate(self.active_sequence):
            x, y = cell
            self.root.after(int(self.display_time * i * 0.7), lambda x=x, y=y: self.highlight_cell(x, y)) # 少し早めに
            self.root.after(int(self.display_time * (i + 1) * 0.7), self.reset_cell_color)

    # --- 難易度調整 ---
    def adjust_time(self, delta):
        new_time = self.display_time + delta
        if 100 <= new_time <= 2000:
            self.display_time = new_time
            self.time_label.config(text=f"Display Time: {self.display_time / 1000:.2f}s")

    # --- Dual N-Back 関連 ---
    def _increase_n_back(self):
        self.n_back_level += 1
        self.n_back_label.config(text=str(self.n_back_level))
        self.n_back_history = deque(maxlen=self.n_back_level)

    def _decrease_n_back(self):
        if self.n_back_level > 1:
            self.n_back_level -= 1
            self.n_back_label.config(text=str(self.n_back_level))
            self.n_back_history = deque(maxlen=self.n_back_level)

if __name__ == "__main__":
    root = tk.Tk()
    trainer = WorkingMemoryTrainer(root)
    root.mainloop()
