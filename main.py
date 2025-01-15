import sys
import json
import logging
from colorama import init as colorama_init

# Import your classes
from models import BotInfo, Scenario
from tournament import Tournament

def setup_logging() -> None:
    """
    Configure logging to console + file.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("tournament.log", mode="w", encoding="utf-8"),
        ],
    )

def main() -> None:
    colorama_init()  # enable color on Windows
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting tournament...")

    # Load scenarios from config.json
    with open("config.json", "r", encoding="utf-8") as f:
        config_data = json.load(f)
    scenarios_data = config_data["scenarios"]
    scenarios = []
    for sc in scenarios_data:
        scenario = Scenario(
            name=sc["name"],
            rows=sc["board_rows"],
            cols=sc["board_cols"],
            initial_positions=sc["initial_positions"]
        )
        scenarios.append(scenario)

    # Load bots from participants.json
    with open("participants.json", "r", encoding="utf-8") as f:
        participants_data = json.load(f)
    bots_data = participants_data["bots"]
    bots = []
    for bd in bots_data:
        bot = BotInfo(name=bd["name"], command=bd["command"])
        bots.append(bot)

    # Create tournament and run
    tournament = Tournament(bots=bots, scenarios=scenarios)
    tournament.run_all_matches(verbose=True, move_timeout=5.0)
    tournament.print_final_standings()

if __name__ == "__main__":
    main()
