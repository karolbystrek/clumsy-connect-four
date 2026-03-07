"""
Comparison: Deterministic vs. Probabilistic Variants.
Algorithm: Negamax (Depth 9, Pruning: True) for both players.
Variants: Deterministic (slip=0.0) vs. Probabilistic (slip=0.1).
Output: output/compare_det_vs_nondet/
"""

from easyAI import Negamax
from game_simulation import GameSimulation

DEPTH_PLAYER_1 = 9
DEPTH_PLAYER_2 = 9
NUM_MATCHES = 20
SLIP_PROBABILITY = 0.1
OUTPUT_NAME = "compare_det_vs_nondet_d9"

simulation = GameSimulation(
    algo_player_1=Negamax(DEPTH_PLAYER_1),
    algo_player_2=Negamax(DEPTH_PLAYER_2),
    num_matches=NUM_MATCHES,
    variants=[
        ("deterministic", 0.0),
        ("probabilistic", SLIP_PROBABILITY),
    ],
    output_name=OUTPUT_NAME,
)

if __name__ == "__main__":
    simulation.run()
