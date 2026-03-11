"""
Expecti-Minimax algorithm with optional alpha-beta pruning for
games with chance nodes (e.g. Clumsy Connect Four with slip probability).

Unlike standard Negamax which treats the game as fully deterministic,
Expectiminimax explicitly models the probability of each outcome
when a move is made, computing expected values at chance nodes.

The tree has three types of nodes:
  - MAX nodes: current player picks the move with highest value
  - MIN nodes: opponent picks the move with lowest value (via negation)
  - CHANCE nodes: after a move is chosen, the value is the
    probability-weighted average over all possible slip outcomes

OPTIMIZATION: Uses in-place board manipulation (make/unmake move)
instead of deepcopy to drastically reduce overhead.
"""

import numpy as np

inf = float("infinity")


def get_slip_outcomes(column, slip_probability, board):
    """
    Given a chosen column, the slip probability, and the current board,
    returns a list of (actual_column, probability) pairs representing
    all possible outcomes of the move.

    This mirrors the logic of ConnectFour.slip() but deterministically
    enumerates all outcomes instead of sampling randomly.
    """
    if slip_probability <= 0.0:
        return [(column, 1.0)]

    # Determine which adjacent columns exist
    adjacent = []
    if column > 0:
        adjacent.append(column - 1)
    if column < 6:
        adjacent.append(column + 1)

    # Filter to adjacent columns that are not full
    valid_adjacent = [c for c in adjacent if board[:, c].min() == 0]

    if not valid_adjacent:
        # Both adjacent columns are full (or don't exist), no slip possible
        return [(column, 1.0)]

    outcomes = []
    # The intended column with probability (1 - slip_probability)
    outcomes.append((column, 1.0 - slip_probability))

    # Each valid adjacent column gets an equal share of slip_probability
    slip_per_col = slip_probability / len(valid_adjacent)
    for adj_col in valid_adjacent:
        outcomes.append((adj_col, slip_per_col))

    return outcomes


def expectiminimax(
    game,
    depth,
    origDepth,
    scoring,
    slip_probability,
    alpha=-inf,
    beta=+inf,
    use_pruning=True,
):
    """
    Expectiminimax with alpha-beta pruning using in-place board manipulation.

    At MAX/MIN nodes, we use standard alpha-beta bounds.
    At CHANCE nodes (after choosing a move, before evaluating its
    probabilistic outcomes), we compute the weighted average.

    The algorithm reads slip_probability from the game object if available,
    allowing it to automatically behave like standard minimax when the game
    is deterministic (slip=0.0) and model chance nodes when probabilistic.
    """
    if (depth == 0) or game.is_over():
        return scoring(game) * (1 + 0.001 * depth)

    possible_moves = game.possible_moves()
    best_move = possible_moves[0]
    if depth == origDepth:
        game.ai_move = possible_moves[0]

    bestValue = -inf

    for move in possible_moves:
        # Evaluate the chance node for this move (in-place, no copy)
        move_value = _evaluate_chance_node(
            game, move, depth, origDepth, scoring,
            slip_probability, alpha, beta, use_pruning,
        )

        if bestValue < move_value:
            bestValue = move_value
            best_move = move

        if alpha < move_value:
            alpha = move_value
            if depth == origDepth:
                game.ai_move = move
            if use_pruning and alpha >= beta:
                break

    return bestValue


def _evaluate_chance_node(
    game, move, depth, origDepth, scoring,
    slip_probability, alpha, beta, use_pruning,
):
    """
    Evaluate a chance node using IN-PLACE board manipulation.

    Instead of deepcopy, we:
    1. Place piece on the board
    2. Switch current_player
    3. Recurse
    4. Undo: restore board cell and switch player back

    This avoids expensive deepcopy at every node.
    """
    outcomes = get_slip_outcomes(move, slip_probability, game.board)

    expected_value = 0.0

    for actual_column, probability in outcomes:
        # --- MAKE MOVE (in-place) ---
        line = np.argmin(game.board[:, actual_column] != 0)
        game.board[line, actual_column] = game.current_player
        # Switch player manually (equivalent to game.switch_player())
        old_player = game.current_player
        game.current_player = 2 if game.current_player == 1 else 1

        # --- RECURSE ---
        if use_pruning:
            child_value = -expectiminimax(
                game, depth - 1, origDepth, scoring,
                slip_probability, -beta, -alpha, True,
            )
        else:
            child_value = -expectiminimax(
                game, depth - 1, origDepth, scoring,
                slip_probability, -inf, +inf, False,
            )

        # --- UNMAKE MOVE (restore state) ---
        game.current_player = old_player
        game.board[line, actual_column] = 0

        expected_value += probability * child_value

    return expected_value


class ExpectiMinimax:
    """
    Expecti-Minimax algorithm for games with chance/probabilistic elements.

    Drop-in replacement for Negamax that explicitly models slip probability
    at chance nodes. Uses in-place board manipulation for performance.

    The algorithm reads slip_probability from the game object (game.slip_probability)
    if available. This means:
    - In deterministic variants (slip=0.0): no chance nodes, behaves like Negamax
    - In probabilistic variants (slip=0.1): models chance nodes properly

    If the game has no slip_probability attribute, uses the value passed at init.

    Parameters
    ----------
    depth : int
        How many moves ahead the AI should search.
    scoring : callable, optional
        Scoring function f(game) -> score. If None, uses game.scoring().
    slip_probability : float
        Fallback slip probability (used if game has no slip_probability attribute).
    win_score : float
        Score above which a position is considered a win.
    use_pruning : bool
        Whether to use alpha-beta pruning (default True).
    """

    def __init__(
        self,
        depth,
        scoring=None,
        slip_probability=0.1,
        win_score=+inf,
        use_pruning=True,
    ):
        self.scoring = scoring
        self.depth = depth
        self.slip_probability = slip_probability
        self.win_score = win_score
        self.use_pruning = use_pruning

    def __call__(self, game):
        """
        Returns the AI's best move given the current state of the game.
        """
        scoring = (
            self.scoring if self.scoring else (lambda g: g.scoring())
        )

        # Use the game's slip_probability if available, otherwise use our own
        slip_prob = getattr(game, "slip_probability", self.slip_probability)

        self.alpha = expectiminimax(
            game,
            self.depth,
            self.depth,
            scoring,
            slip_prob,
            -self.win_score,
            +self.win_score,
            self.use_pruning,
        )
        return game.ai_move
