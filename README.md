# Memory Game

This is a memory game built with Tkinter, where players are challenged to remember the sequence of highlighted cells. As the game progresses, the sequence becomes longer and more difficult to memorize.

## Features

- **Dynamic Difficulty:** The game's difficulty increases with each round by adding more cells to the sequence.
- **Customizable Settings:** Players can adjust the initial display time of cells, the start round, and the duration of the flash for correct or incorrect answers.
- **Score Tracking:** The game tracks the current score and the high score, updating them based on the player's performance.
- **Visual Feedback:** Provides visual feedback for correct and incorrect answers through color changes.

## How to Play

1. Press the **Start** button to begin the game.
2. Memorize the sequence of highlighted cells.
3. Click the cells in the order they were highlighted.
4. The game will indicate a correct sequence with a green flash and an incorrect sequence with a red flash.
5. Adjust the game settings as desired for a personalized experience.

## Configuration Options

- **Size:** Determines the size of the grid.
- **Initial Display Time:** The amount of time each cell is highlighted at the start.
- **Flash Duration:** How long the flash lasts for correct or incorrect answers.
- **Correct/Incorrect Flash Color:** The colors used for flashing feedback.
- **Start Round:** The initial round number, affecting the sequence length at the start of the game.

## Requirements

- Python 3
- Tkinter library

## Setup

Run the script using Python 3. Ensure Tkinter is installed and available in your Python environment.

```bash
python memory_game.py
```

## Contributing

Feel free to fork the repository and submit pull requests to contribute to the development of this memory game.

## License

This project is open-source and available under the MIT License.


# Technical Documentation for Memory Game

## Overview

This document provides a technical overview of the Memory Game developed using Python's Tkinter library. The game challenges players to remember and replicate a sequence of highlighted cells. This section describes the game's main components, their functionality, and how they interact.

## Components

### Main Variables

- `size`: Defines the size of the game grid.
- `initial_display_time`: The initial time in milliseconds each cell is highlighted.
- `flash_duration`: Duration in milliseconds of the flash indicating correct or incorrect answers.
- `correct_flash_color`, `incorrect_flash_color`: Colors used for indicating correct and incorrect answers, respectively.
- `start_round`: Initial round number.

### Global Variables

- `buttons`: A list of lists containing button widgets for each cell in the grid.
- `active_sequence`: The sequence of cells that the player must replicate.
- `user_sequence`: The sequence of cells selected by the player.
- `score`, `high_score`: Variables for tracking the player's current and highest scores.
- `game_active`: Boolean indicating whether the game is currently active.
- `display_time`: Current display time for highlighting cells.
- `last_highlighted`: The last cell that was highlighted, to avoid repetition.

### Functions

#### `highlight_cell(x, y)`

Highlights a specified cell.

#### `reset_cell_color()`

Resets the color of all cells to their default state.

#### `get_random_cell()`

Selects a random cell that has not been the last highlighted.

#### `user_click(x, y)`

Handles user clicks, updating the `user_sequence` and checking against `active_sequence`.

#### `check_sequence()`

Checks if the `user_sequence` matches the `active_sequence` and updates the game state accordingly.

#### `update_score(success)`

Updates the score and provides visual feedback based on whether the user's sequence was correct.

#### `game_over()`

Ends the game and resets the game state.

#### `start_game()`

Initializes the game state and starts a new game.

#### `new_round()`

Starts a new round by adding another cell to the `active_sequence`.

#### `show_sequence()`

Displays the `active_sequence` to the player.

#### `adjust_time(delta)`

Adjusts the display time of the cells.

#### `set_start_round()`

Sets the initial round number based on user input.

#### `reset_game()`

Resets the game to its initial state.

## GUI Layout

The game's GUI is created using Tkinter, with a simple layout consisting of a grid for the cells, a score display, and buttons for starting, resetting, and adjusting settings.

## Running the Game

Ensure Python 3 and Tkinter are installed. Run the script to start the game:

```bash
python memory_game.py
```

## Conclusion

This Memory Game showcases the capabilities of Python's Tkinter library for creating simple yet engaging GUI applications. It demonstrates handling user input, updating the UI, and managing game state and logic.



# メモリーゲーム

このメモリーゲームはTkinterを使用して構築されており、プレイヤーはハイライトされたセルのシーケンスを記憶することに挑戦します。ゲームが進むにつれて、シーケンスはより長く、記憶するのがより難しくなります。

## 特徴

- **動的な難易度:** ゲームの難易度は、シーケンスにセルを追加することで各ラウンドごとに増加します。
- **カスタマイズ可能な設定:** プレイヤーは、セルの初期表示時間、スタートラウンド、正解または不正解のフラッシュの持続時間を調整できます。
- **スコア追跡:** プレイヤーのパフォーマンスに基づいて現在のスコアとハイスコアを追跡し、更新します。
- **視覚的フィードバック:** 正解と不正解に対して色の変化を通じて視覚的フィードバックを提供します。

## 遊び方

1. **スタート**ボタンを押してゲームを始めます。
2. ハイライトされたセルのシーケンスを記憶します。
3. ハイライトされた順序でセルをクリックします。
4. 正しいシーケンスは緑色のフラッシュ、間違ったシーケンスは赤色のフラッシュで示されます。
5. 個人の体験に合わせてゲーム設定を調整します。

## 設定オプション

- **サイズ:** グリッドのサイズを決定します。
- **初期表示時間:** スタート時に各セルがハイライトされる時間。
- **フラッシュ持続時間:** 正解または不正解のフラッシュがどれだけ続くか。
- **正解/不正解のフラッシュ色:** フィードバックのフラッシュに使用される色。
- **スタートラウンド:** ゲーム開始時のラウンド数で、開始時のシーケンス長に影響します。

## 必要条件

- Python 3
- Tkinterライブラリ

## セットアップ

Python 3を使用してスクリプトを実行します。TkinterがPython環境にインストールされていて利用可能であることを確認してください。

```bash
python memory_game.py
```

## 貢献

リポジトリをフォークして、このメモリーゲームの開発に貢献するためのプルリクエストを送信してください。

## ライセンス

このプロジェクトはオープンソースであり、MITライセンスの下で利用可能です。

## コンポーネント

### 主要変数

- `size`: ゲームグリッドのサイズを定義します。
- `initial_display_time`: 各セルがハイライトされる初期時間（ミリ秒）。
- `flash_duration`: 正解または不正解を示すフラッシュの持続時間（ミリ秒）。
- `correct_flash_color`, `incorrect_flash_color`: 正解および不正解を示すために使用される色。
- `start_round`: 初期ラウンド数。

### グローバル変数

- `buttons`: グリッド内の各セルに対するボタンウィジェットを含むリストのリスト。
- `active_sequence`: プレイヤーが再現する必要があるセルのシーケンス。
- `user_sequence`: プレイヤーによって選択されたセルのシーケンス。
- `score`, `high_score`: プレイヤーの現在のスコアと最高スコアを追跡する変数。
- `game_active`: ゲームが現在アクティブかどうかを示すブール値。
- `display_time`: セルをハイライトする現在の表示時間。
- `last_highlighted`: 繰り返しを避けるために最後にハイライトされたセル。

### 関数

#### `highlight_cell(x, y)`

指定されたセルをハイライトします。

#### `reset_cell_color()`

すべてのセルの色をデフォルト状態にリセットします。

#### `get_random_cell()`

最後にハイライトされたものではないランダムなセルを選択します。

#### `user_click(x, y)`

ユーザーのクリックを処理し、`user_sequence`を更新し、`active_sequence`と比較します。

#### `check_sequence()`

`user_sequence`が`active_sequence`と一致するかどうかをチェックし、ゲームの状態をそれに応じて更新します。

#### `update_score(success)`

ユーザーのシーケンスが正しいかどうかに基づいてスコアを更新し、視覚的フィードバックを提供します。

#### `game_over()`

ゲームを終了し、ゲームの状態をリセットします。

#### `start_game()`

ゲームの状態を初期化し、新しいゲームを開始します。

#### `new_round()`

`active_sequence`に別のセルを追加することで、新しいラウンドを開始します。

#### `show_sequence()`

プレイヤーに`active_sequence`を表示します。

#### `adjust_time(delta)`

セルの表示時間を調整します。

#### `set_start_round()`

ユーザー入力に基づいて初期ラウンド数を設定します。

#### `reset_game()`

ゲームを初期状態にリセットします。

## GUIレイアウト

ゲームのGUIはTkinterを使用して作成され、セルのグリッド、スコア表示、およびゲームを開始、リセット、設定を調整するためのボタンを含むシンプルなレイアウトで構成されています。

## ゲームの実行

Python 3とTkinterがインストールされていることを確認します。スクリプトを実行してゲームを開始します：

```bash
python memory_game.py
```
