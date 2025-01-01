import tkinter as tk
import random
import time

class WorkingMemoryTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive Working Memory Trainer")

        # --- ゲーム設定 ---
        self.grid_size = 3
        self.base_display_time = 1000  # 1秒
        self.flash_duration = 500      # 0.5秒
        self.correct_flash_color = "sea green"
        self.incorrect_flash_color = "salmon"

        # ラウンド数は 3〜9 程度に設定
        self.start_round = 3  
        self.max_round = 9

        # 適応的調整用
        self.success_streak = 0
        self.fail_streak = 0

        # --- ゲーム状態変数 ---
        self.buttons = []
        self.active_sequence = []
        self.user_sequence = []
        self.score = 0
        self.high_score = 0
        self.game_active = False
        self.last_highlighted = None
        self.current_round = 0
        self.start_time = 0
        self.reaction_log = []  # 各クリックごとの詳細を保存
        self.high_round = 0  # 最高到達ラウンド数

        # --- GUIセットアップ ---
        self._setup_ui()

    def _setup_ui(self):
        # スコアフレーム
        self.score_frame = tk.Frame(self.root, bg="white")
        self.score_frame.grid(row=0, column=0, columnspan=self.grid_size, sticky="ew")
        self.score_label = tk.Label(self.score_frame, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.pack(pady=5)
        self.high_score_label = tk.Label(self.score_frame, text=f"High Score: {self.high_score}", font=("Helvetica", 12))
        self.high_score_label.pack(pady=0)
        self.high_round_label = tk.Label(self.score_frame, text=f"Best Round: {self.high_round}", font=("Helvetica", 12))
        self.high_round_label.pack(pady=0)

        # マス目ボタンの作成
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                button = tk.Button(
                    self.root, bg="dark gray", width=8, height=4,
                    command=lambda x=i, y=j: self.user_click(x, y)
                )
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

        # フィードバックラベル
        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.feedback_label.grid(row=self.grid_size + 2, column=0, columnspan=self.grid_size)

    def highlight_cell(self, x, y):
        self.buttons[x][y].config(bg="light sky blue")

    def reset_cell_color(self):
        for row in self.buttons:
            for button in row:
                button.config(bg="dark gray")

    def get_random_cell(self):
        while True:
            cell = (
                random.randint(0, self.grid_size - 1),
                random.randint(0, self.grid_size - 1)
            )
            if cell != self.last_highlighted:
                self.last_highlighted = cell
                return cell

    def user_click(self, x, y):
        if not self.game_active:
            return

        timestamp = time.time()
        rt = timestamp - self.start_time
        index_in_seq = len(self.user_sequence)

        correct = (x, y) == self.active_sequence[index_in_seq]
        self.reaction_log.append({
            "round": self.current_round,
            "index_in_sequence": index_in_seq,
            "clicked_cell": (x, y),
            "correct_cell": self.active_sequence[index_in_seq],
            "correct": correct,
            "reaction_time": rt
        })

        self.user_sequence.append((x, y))

        if not correct:
            self.feedback_label.config(text="Incorrect!", fg="red")
            self.game_over()
        else:
            if len(self.user_sequence) == len(self.active_sequence):
                self.check_sequence()

    def check_sequence(self):
        self.feedback_label.config(text="Correct!", fg="green")
        self.score += 1
        self.update_score(success=True)

        self.success_streak += 1
        self.fail_streak = 0

        if self.success_streak >= 2:
            self.current_round += 1
            self.success_streak = 0

        if self.current_round > self.max_round:
            self.current_round = self.max_round

        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")

        self.root.after(800, self.new_round)

    def update_score(self, success):
        if success:
            self.score_frame.config(bg=self.correct_flash_color)
            self.root.after(self.flash_duration, lambda: self.score_frame.config(bg="white"))
            self.score_label.config(text=f"Score: {self.score}", fg="forest green")
        else:
            self.score_label.config(text=f"Score: {self.score}", fg="firebrick")
            self.score_frame.config(bg=self.incorrect_flash_color)
            self.root.after(self.flash_duration, lambda: self.score_frame.config(bg="white"))

    def game_over(self):
        self.game_active = False
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.reset_cell_color()

        self.fail_streak += 1
        self.success_streak = 0

        if self.current_round > self.high_round:
            self.high_round = self.current_round
            self.high_round_label.config(text=f"Best Round: {self.high_round}")

        # 反応ログの集計
        if len(self.reaction_log) > 0:
            correct_trials = [r for r in self.reaction_log if r["correct"]]
            if len(correct_trials) > 0:
                accuracy = len(correct_trials) / len(self.reaction_log)
                avg_rt = sum(r["reaction_time"] for r in correct_trials) / len(correct_trials)
                print(f"Accuracy: {accuracy*100:.2f}%, Avg RT: {avg_rt:.3f}s")
            else:
                print("No correct trials. Accuracy: 0.00%, Avg RT: N/A")
        else:
            print("No trials recorded.")

        self.active_sequence.clear()
        self.user_sequence.clear()
        self.reaction_log.clear()

    def reset_game(self):
        self.game_over()
        self.score = 0
        self.update_score(success=True)
        self.feedback_label.config(text="")
        self.reaction_log.clear()
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.current_round = self.start_round
        self.high_round = 0
        self.high_round_label.config(text=f"Best Round: {self.high_round}")

    def new_round(self):
        if not self.game_active:
            return
        self.user_sequence = []

        if self.fail_streak >= 2:
            self.current_round -= 1
            if self.current_round < self.start_round:
                self.current_round = self.start_round
            self.fail_streak = 0

        self.active_sequence = [self.get_random_cell() for _ in range(self.current_round)]
        self.show_sequence()

    def show_sequence(self):
        self.reset_cell_color()
        self.start_time = time.time()
        for i, cell in enumerate(self.active_sequence):
            x, y = cell
            self.root.after(int(self.base_display_time * i), \
                            lambda x=x, y=y: self.highlight_cell(x, y))
            self.root.after(int(self.base_display_time * (i + 1)), \
                            self.reset_cell_color)

    def start_game(self):
        self.current_round = self.start_round
        self.score = 0
        self.success_streak = 0
        self.fail_streak = 0
        self.update_score(success=True)
        self.game_active = True
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)

        self.active_sequence = [self.get_random_cell() for _ in range(self.current_round)]
        self.show_sequence()

if __name__ == "__main__":
    root = tk.Tk()
    trainer = WorkingMemoryTrainer(root)
    root.mainloop()
