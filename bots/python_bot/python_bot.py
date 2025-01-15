#!/usr/bin/env python
import sys
import json
import random

def find_random_empty_cell(board):
    """
    Возвращает (row, col) случайной пустой клетки, или None, если пустых нет.
    board — список списков, где "" означает пустоту, "X"/"O" — занятые клетки.
    """
    empty_cells = []
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == "":
                empty_cells.append((r, c))
    if not empty_cells:
        return None
    return random.choice(empty_cells)

def main():
    # Считываем все данные из stdin (как строку)
    input_data_str = sys.stdin.read()

    # Парсим JSON
    try:
        input_json = json.loads(input_data_str)
    except json.JSONDecodeError:
        # Если данные невалидны — выходим или выводим ошибку
        # Но в рамках конкурса просто завершим программу.
        print(json.dumps({"error": "invalid JSON"}))
        return

    # Извлекаем необходимые поля
    board = input_json.get("board", [])
    my_symbol = input_json.get("mySymbol", "X")
    # opponent_symbol = input_json.get("opponentSymbol", "O")  # можем использовать, если нужно

    # Ищем случайную пустую клетку
    chosen_cell = find_random_empty_cell(board)
    if chosen_cell is None:
        # Если нет пустых клеток, вернём ошибку или "пас" (но в "пять в ряд" такого обычно нет)
        # Для примера возвращаем -1,-1, хотя движок нас точно дисквалифицирует
        move_response = {
            "move": {"row": -1, "col": -1},
            "debug": "No empty cells available"
        }
    else:
        row, col = chosen_cell
        move_response = {
            "move": {"row": row, "col": col},
            "debug": f"Random move for {my_symbol}"
        }

    # Выводим ответ в stdout (JSON)
    print(json.dumps(move_response))

if __name__ == "__main__":
    main()
