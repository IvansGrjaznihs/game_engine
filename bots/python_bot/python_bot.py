#!/usr/bin/env python
import sys
import json
import random

def find_random_empty_cell(board):
    """
    Return (row, col) of a random empty cell in the board. If there are no empty cells, return None.
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
    # Read input JSON from stdin (as string)
    input_data_str = sys.stdin.read()

    # JSON parsing
    try:
        input_json = json.loads(input_data_str)
    except json.JSONDecodeError:
        # If input is not a valid JSON, return an error message in JSON format
        # (instead of raising an exception, as it would be caught by the engine)
        print(json.dumps({"error": "invalid JSON"}))
        return

    # Get the board and my symbol from the input JSON
    board = input_json.get("board", [])
    my_symbol = input_json.get("mySymbol", "X")
    # opponent_symbol = input_json.get("opponentSymbol", "O")  # можем использовать, если нужно

    # Get a random empty cell
    chosen_cell = find_random_empty_cell(board)
    if chosen_cell is None:
        # If there are no empty cells, return an error message in JSON format
        # For the "move" field, return (-1, -1) to indicate that there are no moves available
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

    # Output the move response in JSON format
    print(json.dumps(move_response))

if __name__ == "__main__":
    main()
