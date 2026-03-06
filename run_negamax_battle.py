from easyAI import Negamax

from game_simulation import GameSimulation

DEPTH_PLAYER_1 = 5
DEPTH_PLAYER_2 = 5
NUM_MATCHES = 100
SLIP_PROBABILITY = 0.1

simulation = GameSimulation(
    algo_player_1=Negamax(DEPTH_PLAYER_1),
    algo_player_2=Negamax(DEPTH_PLAYER_2),
    num_matches=NUM_MATCHES,
    variants=[
        ("deterministic", 0.0),
        ("probabilistic", SLIP_PROBABILITY),
    ],
    output_name="negamax_battle",
)

if __name__ == "__main__":
    simulation.run()
