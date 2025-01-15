import re
from typing import List, Dict, Any, Optional, Tuple
from colorama import Fore, Style

# Regex for stripping ANSI codes
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")


class BotInfo:
    """
    Represents a participant (bot) with a name and a shell command.
    """
    def __init__(self, name: str, command: str):
        self.name = name
        self.command = command

    def __repr__(self) -> str:
        return f"BotInfo(name={self.name}, command={self.command})"


class Scenario:
    """
    Represents a game scenario with a name, board size, and initial placements.
    """
    def __init__(self, name: str, rows: int, cols: int, initial_positions: List[Dict[str, Any]]):
        self.name = name
        self.rows = rows
        self.cols = cols
        self.initial_positions = initial_positions

    def __repr__(self) -> str:
        return (f"Scenario(name={self.name}, rows={self.rows}, cols={self.cols}, "
                f"initial_positions={len(self.initial_positions)} positions)")


def color_cell(
    cell_value: str,
    is_winning: bool,
    width: int = 3
) -> str:
    """
    Returns a color-formatted cell with a fixed width for alignment.
    If `is_winning` is True, color is green. Otherwise:
      - X = red
      - O = blue
      - empty = gray
    """
    if cell_value == "X":
        color_char = Fore.GREEN + "X" + Style.RESET_ALL if is_winning else Fore.RED + "X" + Style.RESET_ALL
    elif cell_value == "O":
        color_char = Fore.GREEN + "O" + Style.RESET_ALL if is_winning else Fore.BLUE + "O" + Style.RESET_ALL
    else:
        color_char = Fore.GREEN + "." + Style.RESET_ALL if is_winning else Fore.LIGHTBLACK_EX + "." + Style.RESET_ALL

    # Strip ANSI to measure length
    raw_char = ANSI_PATTERN.sub('', color_char)  # e.g. "X"
    visible_len = len(raw_char)  # typically 1
    spaces_needed = max(0, width - visible_len)
    return (" " * spaces_needed) + color_char
