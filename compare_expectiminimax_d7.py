"""
Comparison: ExpectiMinimax vs. Negamax (Depth 7).
Algorithms: ExpectiMinimax (slip-aware, AB pruning) vs. Negamax (AB pruning).
Depth: 7.
Variants: Deterministic, Probabilistic (slip=0.1).
Output: output/expectiminimax_vs_negamax_d7/
"""

from easyAI import Negamax
from easyAI.AI.ExpectiMinimax import ExpectiMinimax
from game_simulation import GameSimulation

DEPTH = 7
NUM_MATCHES = 20
SLIP_PROBABILITY = 0.1
OUTPUT_NAME = "expectiminimax_vs_negamax_d7"

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
