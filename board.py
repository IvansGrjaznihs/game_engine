import os
import time
from typing import List, Tuple, Optional
from models import color_cell  # relative import of color_cell
# or from models import color_cell if in the same folder without __init__.py

class Board:
    """
    Encapsulates the 2D board and related operations:
    - Creating / printing
    - Checking if full
    - Checking for 5 in a row
    """
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid: List[List[str]] = [["" for _ in range(cols)] for _ in range(rows)]

    def place_symbol(self, row: int, col: int, symbol: str) -> None:
        """
        Place a symbol (e.g., 'X', 'O') at (row, col).
        Caller must ensure it's valid and empty beforehand.
        """
        self.grid[row][col] = symbol

    def is_full(self) -> bool:
        """True if no empty cells remain."""
        for row in self.grid:
            for cell in row:
                if cell == "":
                    return False
        return True

    def find_five_in_a_row(
        self, row: int, col: int, symbol: str
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Check if placing `symbol` at (row, col) yields 5 in a row.
        Returns a list of positions if found, else None.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        def get_line_positions(r_step: int, c_step: int):
            positions = [(row, col)]
            # forward
            r, c = row + r_step, col + c_step
            while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == symbol:
                positions.append((r, c))
                r += r_step
                c += c_step
            # backward
            r, c = row - r_step, col - c_step
            while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == symbol:
                positions.append((r, c))
                r -= r_step
                c -= c_step
            return positions

        for dr, dc in directions:
            line = get_line_positions(dr, dc)
            if len(line) >= 5:
                return line
        return None

    def clear_console(self) -> None:
        """
        Clears the console (Windows, macOS, Linux).
        """
        time.sleep(0.3)

        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
            
    def print_board(self, winning_positions: Optional[List[Tuple[int,int]]] = None) -> None:
        """
        Print the board with optional highlight of winning_positions in green.
        """
        if winning_positions is None:
            winning_positions = []
        winning_set = set(winning_positions)

        # Column header
        print("    ", end="")
        for c in range(self.cols):
            print(f"{c:3}", end="")
        print()

        # Each row
        for r in range(self.rows):
            print(f"{r:3} ", end="")
            for c in range(self.cols):
                is_win = (r, c) in winning_set
                cell_str = color_cell(self.grid[r][c], is_winning=is_win, width=3)
                print(cell_str, end="")
            print()
        print()
