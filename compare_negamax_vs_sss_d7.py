"""
Comparison: Negamax vs. SSS* Algorithm (Depth 7).
Algorithms: Negamax (AB Pruning) vs. SSS*.
Depth: 7.
Variants: Deterministic, Probabilistic (slip=0.1).
Output: output/negamax_vs_sss_d7/
"""

from easyAI import Negamax, SSS
from game_simulation import GameSimulation

DEPTH = 7
NUM_MATCHES = 20
SLIP_PROBABILITY = 0.1
OUTPUT_NAME = "negamax_vs_sss_d7"

simulation = GameSimulation(
    algo_player_1=Negamax(DEPTH),
    algo_player_2=SSS(DEPTH),
    num_matches=NUM_MATCHES,
    variants=[
        ("deterministic", 0.0),
        ("probabilistic", SLIP_PROBABILITY),
    ],
    output_name=OUTPUT_NAME,
)

if __name__ == "__main__":
    simulation.run()
