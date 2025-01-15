import logging
from typing import List
from itertools import combinations

from models import BotInfo, Scenario
from engine import GameEngine

logger = logging.getLogger(__name__)

class Tournament:
    """
    Conducts a round-robin tournament among multiple bots and scenarios.
    """

    def __init__(self, bots: List[BotInfo], scenarios: List[Scenario]):
        self.bots = bots
        self.scenarios = scenarios
        self.score_table = {bot.name: 0 for bot in bots}  # e.g. {"PythonBot": 0, "CSharpBot": 0}

    def run_all_matches(self, verbose: bool = True, move_timeout: float = 5.0) -> None:
        """
        For each pair of bots, for each scenario, run two matches (switching first player).
        Update scores accordingly.
        """
        bot_pairs = list(combinations(self.bots, 2))
        for bot1, bot2 in bot_pairs:
            for scenario in self.scenarios:
                for first_player in [1, 2]:
                    logger.info(f"Match: {bot1.name} vs {bot2.name}, scenario={scenario.name}, first={first_player}")
                    if verbose:
                        print(f"\n--- Scenario {scenario.name} ({scenario.rows}x{scenario.cols}), "
                              f"first = {bot1.name if first_player == 1 else bot2.name} ---")
                    engine = GameEngine(bot1, bot2, scenario, first_player)
                    result = engine.run_game(verbose=verbose, move_timeout=move_timeout)
                    self.update_scores(bot1, bot2, result)

    def update_scores(self, bot1: BotInfo, bot2: BotInfo, result: int) -> None:
        """
        3 points for a win, 1 point each for a draw, 0 for a loss.
        """
        if result == 1:
            self.score_table[bot1.name] += 3
        elif result == 2:
            self.score_table[bot2.name] += 3
        else:
            self.score_table[bot1.name] += 1
            self.score_table[bot2.name] += 1

    def print_final_standings(self) -> None:
        """
        Prints final scoreboard, sorted descending by points.
        """
        sorted_scores = sorted(self.score_table.items(), key=lambda x: x[1], reverse=True)
        print("\n=== FINAL SCORES ===")
        for rank, (bot_name, points) in enumerate(sorted_scores, start=1):
            print(f"{rank}. {bot_name} = {points} points")
