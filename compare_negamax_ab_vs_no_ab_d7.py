"""
Comparison: Negamax with Alpha-Beta Pruning vs. Negamax without Pruning (Depth 7).
Algorithms: Negamax (Pruning: True) vs. Negamax (Pruning: False).
Depth: 7.
Variants: Deterministic, Probabilistic (slip=0.1).
Output: output/negamax_ab_vs_no_ab_d7/
"""

from easyAI import Negamax
from game_simulation import GameSimulation

DEPTH = 7
NUM_MATCHES = 5
SLIP_PROBABILITY = 0.1

OUTPUT_NAME = "negamax_ab_vs_no_ab_d7"

simulation = GameSimulation(
    algo_player_1=Negamax(DEPTH, use_pruning=True),
    algo_player_2=Negamax(DEPTH, use_pruning=False),
    num_matches=NUM_MATCHES,
    variants=[
        ("deterministic", 0.0),
        ("probabilistic", SLIP_PROBABILITY),
    ],
    output_name=OUTPUT_NAME,
)

if __name__ == "__main__":
    simulation.run()
