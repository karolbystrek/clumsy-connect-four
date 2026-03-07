"""
Comparison: Negamax Depth 7 vs. Negamax Depth 9.
Algorithms: Negamax (Depth 7) vs. Negamax (Depth 9).
Pruning: Enabled (True).
Variants: Deterministic, Probabilistic (slip=0.1).
Output: output/negamax_depth_7_vs_9/
"""

from easyAI import Negamax
from game_simulation import GameSimulation

DEPTH_1 = 7
DEPTH_2 = 9
NUM_MATCHES = 20
SLIP_PROBABILITY = 0.1
OUTPUT_NAME = "negamax_depth_7_vs_9"

simulation = GameSimulation(
    algo_player_1=Negamax(DEPTH_1),
    algo_player_2=Negamax(DEPTH_2),
    num_matches=NUM_MATCHES,
    variants=[
        ("deterministic", 0.0),
        ("probabilistic", SLIP_PROBABILITY),
    ],
    output_name=OUTPUT_NAME,
)

if __name__ == "__main__":
    simulation.run()
