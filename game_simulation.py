import json
import os
import sys
from datetime import datetime

from clumsy_connect_four import ConnectFour
from easyAI import AI_Player


class GameSimulation:
    def __init__(
        self,
        algo_player_1,
        algo_player_2,
        num_matches,
        variants,
        output_name,
        output_dir="output",
    ):
        self.algo_player_1 = algo_player_1
        self.algo_player_2 = algo_player_2
        self.num_matches = num_matches
        self.variants = variants
        self.output_name = output_name
        self.output_dir = output_dir

    def _get_algo_info(self, algo):
        name = algo.__class__.__name__
        params = []
        if hasattr(algo, "depth"):
            params.append(f"depth={algo.depth}")
        if hasattr(algo, "use_pruning"):
            params.append(f"pruning={algo.use_pruning}")
        if hasattr(algo, "slip_probability"):
            params.append(f"slip={algo.slip_probability}")
        return f"{name}({', '.join(params)})"

    def run(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        algo_1_info = self._get_algo_info(self.algo_player_1)
        algo_2_info = self._get_algo_info(self.algo_player_2)
        configurations = []

        print(f"Running simulation: {self.output_name}")
        print(f"Player 1: {algo_1_info}")
        print(f"Player 2: {algo_2_info}")
        print(f"Matches per variant: {self.num_matches}")

        for variant_name, slip_prob in self.variants:
            print(f"\nRunning {variant_name} variant (slip={slip_prob})...")
            sys.stdout.flush()

            results = self._run_variant(variant_name, slip_prob)
            config = {
                "variant": variant_name,
                "slip_probability": slip_prob,
                "results": results,
            }

            self._print_results(config)
            configurations.append(config)

        all_results = {
            "timestamp": timestamp,
            "num_matches": self.num_matches,
            "player_1_algo": algo_1_info,
            "player_2_algo": algo_2_info,
            "configurations": configurations,
        }

        self._save_results(all_results, timestamp)

    def _run_match(self, slip_probability, player_1_starts):
        player_1 = AI_Player(self.algo_player_1, name="Player 1")
        player_2 = AI_Player(self.algo_player_2, name="Player 2")

        players = [player_1, player_2] if player_1_starts else [player_2, player_1]
        game = ConnectFour(players, slip_probability=slip_probability)
        game.play()

        winner = None
        if game.lose():
            winner = game.opponent

        return winner, player_1, player_2

    def _run_variant(self, variant_name, slip_probability):
        results = {"player_1_wins": 0, "player_2_wins": 0, "draws": 0}
        all_move_times = {"player_1": [], "player_2": []}

        for match_num in range(self.num_matches):
            player_1_starts = match_num % 2 == 0
            winner, player_1, player_2 = self._run_match(
                slip_probability, player_1_starts
            )

            if winner is player_1:
                results["player_1_wins"] += 1
            elif winner is player_2:
                results["player_2_wins"] += 1
            else:
                results["draws"] += 1

            all_move_times["player_1"].extend(player_1.move_times)
            all_move_times["player_2"].extend(player_2.move_times)

        for player in ("player_1", "player_2"):
            times = all_move_times[player]
            key = f"avg_move_time_{player}"
            results[key] = sum(times) / len(times) if times else 0.0

        return results

    def _print_results(self, config):
        print(f"\n{'=' * 60}")
        print(f"  Variant: {config['variant']}")
        print(f"  Slip probability: {config['slip_probability']}")
        print(f"{'=' * 60}")
        r = config["results"]
        print(f"  Player 1 wins:           {r['player_1_wins']}")
        print(f"  Player 2 wins:           {r['player_2_wins']}")
        print(f"  Draws:                   {r['draws']}")
        print(f"  Avg move time Player 1:  {r['avg_move_time_player_1']:.4f}s")
        print(f"  Avg move time Player 2:  {r['avg_move_time_player_2']:.4f}s")
        print(f"{'=' * 60}")

    def _save_results(self, all_results, timestamp):
        target_dir = os.path.join(self.output_dir, self.output_name)
        os.makedirs(target_dir, exist_ok=True)
        filename = f"{timestamp}.json"
        filepath = os.path.join(target_dir, filename)

        with open(filepath, "w") as f:
            json.dump(all_results, f, indent=2)

        print(f"\nResults saved to: {filepath}")
