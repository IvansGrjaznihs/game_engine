import json
import subprocess
from typing import Dict, Any, Optional
import logging

from board import Board
from models import BotInfo, Scenario

logger = logging.getLogger(__name__)

class GameEngine:
    """
    Runs a single 'Five in a Row' match between two bots on a given scenario.
    """

    def __init__(
        self,
        bot1: BotInfo,
        bot2: BotInfo,
        scenario: Scenario,
        first_player: int,
    ):
        self.bot1 = bot1
        self.bot2 = bot2
        self.scenario = scenario
        self.first_player = first_player
        self.board = Board(self.scenario.rows, self.scenario.cols)
        self.bot1_symbol = "X"
        self.bot2_symbol = "O"
        self.current_symbol: Optional[str] = None
        self.opponent_symbol: Optional[str] = None

    def setup_board(self) -> None:
        """
        Initialize the board with scenario's initial positions (if any).
        """
        for pos in self.scenario.initial_positions:
            r = pos["row"]
            c = pos["col"]
            s = pos["symbol"]
            self.board.place_symbol(r, c, s)

    def run_game(self, verbose: bool = True, move_timeout: float = 5.0) -> int:
        """
        Play a single match between bot1 & bot2 on the scenario.
        Returns:
          1 => bot1 wins
          2 => bot2 wins
          0 => draw
        """
        # Decide who is first
        current_bot = self.bot1 if self.first_player == 1 else self.bot2
        self.current_symbol = self.bot1_symbol if self.first_player == 1 else self.bot2_symbol
        self.opponent_symbol = self.bot2_symbol if self.first_player == 1 else self.bot1_symbol

        last_move_opponent = None
        move_number = 1

        self.setup_board()

        if verbose:
            print(f"=== Start Game: {self.bot1.name} vs {self.bot2.name}, first: {current_bot.name} ===\n")
            self.board.print_board()

        # Main loop
        while True:
            input_data = {
                "boardSize": self.board.rows,
                "board": self.board.grid,
                "mySymbol": self.current_symbol,
                "opponentSymbol": self.opponent_symbol,
                "lastMoveOpponent": last_move_opponent,
                "moveNumber": move_number,
            }

            # Call the bot
            try:
                bot_response = self.call_bot(current_bot.command, input_data, timeout_sec=move_timeout)
            except Exception as e:
                # Disqualify current bot => other wins
                winner = 2 if current_bot == self.bot1 else 1
                if verbose:
                    print(f"{current_bot.name} disqualified: {e}")
                return winner

            move_obj = bot_response.get("move", {})
            row = move_obj.get("row", -1)
            col = move_obj.get("col", -1)

            # Validate
            if not self.is_valid_move(row, col):
                # Disqualify
                winner = 2 if current_bot == self.bot1 else 1
                if verbose:
                    print(f"Invalid move from {current_bot.name} => disqualified.")
                return winner

            # Place
            self.board.place_symbol(row, col, self.current_symbol)

            # Check for win
            winning_line = self.board.find_five_in_a_row(row, col, self.current_symbol)
            if winning_line:
                if verbose:
                    print(f"Move {current_bot.name} ({self.current_symbol}): row={row}, col={col} => WIN!")
                    self.board.print_board(winning_line)
                return 1 if current_bot == self.bot1 else 2

            # Check for draw
            if self.board.is_full():
                if verbose:
                    print(f"Move {current_bot.name} ({self.current_symbol}): row={row}, col={col} => DRAW!")
                    self.board.print_board()
                return 0

            # Print move
            if verbose:
                print(f"Move {current_bot.name} ({self.current_symbol}): row={row}, col={col}")
                self.board.print_board()

            # Switch turns
            last_move_opponent = {"row": row, "col": col}
            if current_bot == self.bot1:
                current_bot = self.bot2
                self.current_symbol = self.bot2_symbol
                self.opponent_symbol = self.bot1_symbol
            else:
                current_bot = self.bot1
                self.current_symbol = self.bot1_symbol
                self.opponent_symbol = self.bot2_symbol

            move_number += 1

    @staticmethod
    def call_bot(command: str, input_data: Dict[str, Any], timeout_sec: float) -> Dict[str, Any]:
        """
        Execute the bot's process, passing JSON in stdin, reading JSON from stdout.
        Raises if the bot times out or returns invalid JSON / non-zero code.
        """
        input_str = json.dumps(input_data)

        process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
            stdout_data, stderr_data = process.communicate(input=input_str, timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            process.kill()
            raise RuntimeError(f"Bot timed out after {timeout_sec}s")

        if process.returncode != 0:
            raise RuntimeError(f"Bot crashed with code={process.returncode}\nStderr:\n{stderr_data}")

        try:
            response_data = json.loads(stdout_data)
        except json.JSONDecodeError:
            raise RuntimeError(f"Bot returned invalid JSON:\n{stdout_data}")

        return response_data

    def is_valid_move(self, row: int, col: int) -> bool:
        """
        True if (row, col) is within range and cell is empty.
        """
        if not (0 <= row < self.board.rows and 0 <= col < self.board.cols):
            return False
        if self.board.grid[row][col] != "":
            return False
        return True
