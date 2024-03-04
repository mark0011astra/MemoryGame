import tkinter as tk
import random

# ゲームの設定
size = 3
initial_display_time = 600  # 初期のマス表示時間（ミリ秒）
flash_duration = 500         # 正解・不正解時のフラッシュの持続時間（ミリ秒）
correct_flash_color = "yellow green"  # 正解時のフラッシュ色
incorrect_flash_color = "red"  # 不正解時のフラッシュ色
start_round = 1              # ゲーム開始時のラウンド数

# グローバル変数
buttons = []
active_sequence = []
user_sequence = []
score = 0
high_score = 0
game_active = False
display_time = initial_display_time  # 現在のマス表示時間
last_highlighted = None  # 最後に光ったマス

# マスを光らせる関数
def highlight_cell(x, y):
    buttons[x][y].config(bg="light gray")

# 全てのマスの色をリセットする関数
def reset_cell_color():
    for row in buttons:
        for button in row:
            button.config(bg="dark gray")

# ランダムなマスを取得する関数
def get_random_cell():
    global last_highlighted
    while True:
        cell = random.randint(0, size - 1), random.randint(0, size - 1)
        if cell != last_highlighted:
            last_highlighted = cell
            return cell

# ユーザーのクリックを処理する関数
def user_click(x, y):
    global user_sequence, game_active
    if not game_active:
        return
    user_sequence.append((x, y))
    if user_sequence[-1] != active_sequence[len(user_sequence) - 1]:
        update_score(success=False)
        game_over()
    elif len(user_sequence) == len(active_sequence):
        check_sequence()

# シーケンスをチェックする関数
def check_sequence():
    global score, user_sequence, active_sequence, game_active, high_score
    score = len(active_sequence)  # スコアを現在のラウンド数に更新
    update_score(success=True)
    if score > high_score:
        high_score = score
        high_score_label.config(text=f"High Score: {high_score}")
    root.after(1000, new_round)

# スコアを更新する関数
def update_score(success):
    global score_frame
    if success:
        score_frame.config(bg=correct_flash_color)
        root.after(flash_duration, lambda: score_frame.config(bg="white"))
        score_label.config(text=f"Score: {score}", fg="green")
    else:
        score_label.config(text=f"Score: {score}", fg="red")
        score_frame.config(bg=incorrect_flash_color)
        root.after(flash_duration, lambda: score_frame.config(bg="white"))

# ゲームオーバーの処理をする関数
def game_over():
    global game_active, active_sequence, user_sequence
    game_active = False
    start_button.config(state=tk.NORMAL)
    reset_button.config(state=tk.DISABLED)
    reset_cell_color()
    active_sequence = []
    user_sequence = []

# ゲームを開始する関数
def start_game():
    global score, game_active, start_round, active_sequence
    score = 0
    update_score(success=True)
    game_active = True
    start_button.config(state=tk.DISABLED)
    reset_button.config(state=tk.NORMAL)
    active_sequence = [get_random_cell() for _ in range(start_round)]
    show_sequence()

# 新しいラウンドを始める関数
def new_round():
    global user_sequence
    if not game_active:
        return
    user_sequence = []
    active_sequence.append(get_random_cell())
    show_sequence()

# シーケンスを表示する関数
def show_sequence():
    reset_cell_color()
    for i, (x, y) in enumerate(active_sequence):
        root.after(display_time * i, lambda x=x, y=y: highlight_cell(x, y))
        root.after(display_time * (i + 1), reset_cell_color)

# 表示時間を調整する関数
def adjust_time(delta):
    global display_time
    new_time = display_time + delta
    if 0 <= new_time <= 2000:
        display_time = new_time
    time_label.config(text=f"Display Time: {display_time / 1000}s")

# 開始ラウンドを設定する関数
def set_start_round():
    global start_round
    try:
        round_value = int(start_round_entry.get())
        if round_value > 0:
            start_round = round_value
            start_round_label.config(text=f"Start Round: {start_round}")
    except ValueError:
        pass

# ゲームをリセットする関数
def reset_game():
    global game_active, active_sequence, user_sequence, score
    game_active = False
    start_button.config(state=tk.NORMAL)
    reset_button.config(state=tk.DISABLED)
    reset_cell_color()
    active_sequence = []
    user_sequence = []
    score = 0
    update_score(success=True)

# GUIの設定
root = tk.Tk()
root.title("Memory Game")

# スコアフレーム
score_frame = tk.Frame(root, bg="white")
score_frame.grid(row=0, column=0, columnspan=size, sticky="ew")

# スコアラベル
score_label = tk.Label(score_frame, text=f"Score: {score}", font=("Helvetica", 16))
score_label.pack(pady=10)

# ハイスコアラベル
high_score_label = tk.Label(score_frame, text=f"High Score: {high_score}", font=("Helvetica", 16))
high_score_label.pack(pady=10)

# ボタンの作成
for i in range(size):
    row = []
    for j in range(size):
        button = tk.Button(root, bg="dark gray", width=10, height=5, command=lambda x=i, y=j: user_click(x, y))
        button.grid(row=i + 1, column=j)
        row.append(button)
    buttons.append(row)

# スタートボタン
start_button = tk.Button(root, text="Start", command=start_game)
start_button.grid(row=size + 1, column=0, columnspan=size // 2)

# リセットボタン
reset_button = tk.Button(root, text="Reset", command=reset_game, state=tk.DISABLED)
reset_button.grid(row=size + 1, column=size // 2, columnspan=size // 2)

# 表示時間ラベル
time_label = tk.Label(root, text=f"Display Time: {display_time / 1000}s")
time_label.grid(row=size + 2, column=0, columnspan=size)

# 時間調整ボタン
time_up_button = tk.Button(root, text="+", command=lambda: adjust_time(100))
time_up_button.grid(row=size + 3, column=0)

time_down_button = tk.Button(root, text="-", command=lambda: adjust_time(-100))
time_down_button.grid(row=size + 3, column=1)

# 開始ラウンド設定エリア
start_round_frame = tk.Frame(root)
start_round_frame.grid(row=size + 4, column=0, columnspan=size)
start_round_label = tk.Label(start_round_frame, text=f"Start Round: {start_round}")
start_round_label.pack(side=tk.LEFT)
start_round_entry = tk.Entry(start_round_frame, width=5)
start_round_entry.pack(side=tk.LEFT)
start_round_button = tk.Button(start_round_frame, text="Set", command=set_start_round)
start_round_button.pack(side=tk.LEFT)

root.mainloop()

