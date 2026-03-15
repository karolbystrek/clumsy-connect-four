
from easyAI import Negamax
from easyAI.AI.ExpectiMinimax import ExpectiMinimax
from game_simulation import GameSimulation

DEPTH = 4
NUM_MATCHES = 10
SLIP_PROBABILITY = 0.1
OUTPUT_NAME = "expectiminimax_vs_negamax_d4"

simulation = GameSimulation(
    algo_player_1=ExpectiMinimax(DEPTH, slip_probability=SLIP_PROBABILITY),
    algo_player_2=Negamax(DEPTH),
    num_matches=NUM_MATCHES,
    variants=[
        ("deterministic", 0.0),
        ("probabilistic", SLIP_PROBABILITY),
    ],
    output_name=OUTPUT_NAME,
)

if __name__ == "__main__":
    simulation.run()
