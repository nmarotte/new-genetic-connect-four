import random

import Players.MinMaxPlayer as MinMaxPlayer
import Players.RandomPlayer as RandomPlayer
import Players.Player as Player
from game import Connect4Game


def get_random_hypothetical_game_history():
    """
    Constructs a game by making an agent play against himself (since he is random, his turn id
    doesn't matter)
    :return:
    """
    game = Connect4Game()
    player = RandomPlayer.RandomPlayer(3 - game.get_turn())
    while game.get_win() is None:
        placement = player.choose_action(game)
        if placement is not None:
            game.place(placement)
    return game.history


def get_minmax_game_history(difficulty=2):
    """
    Constructs a game by making a minmax agent play against another minmax agent
    :param difficulty:
    :return:
    """
    game = Connect4Game()
    player_a = MinMaxPlayer.MinMaxPlayer(3 - game.get_turn())
    player_b = MinMaxPlayer.MinMaxPlayer(3 - player_a.player_turn_id)
    while game.get_win() is None:
        placement = player_a.choose_action(game, difficulty)
        game.place(placement)
        if game.get_win() is None:
            break

        placement = player_b.choose_action(game, difficulty)
        game.place(placement)
    return game.history


def compute_fitness(player: Player.Player):
    """
    Compute the fitness of the agent. This is done by playing 10 times against a minmax player
    followed by 10 other games against a random player to differentiate agents with low but
    better than random reasoning
    :return: the score
    """
    game = Connect4Game()
    score = 1
    for _ in range(10):
        adversary = MinMaxPlayer.MinMaxPlayer(random.randint(1, 2))
        winner = player.play_against(adversary, game)
        if winner == player.player_turn_id:
            score += 1
    for _ in range(10):
        adversary = RandomPlayer.RandomPlayer(random.randint(1, 2))
        winner = player.play_against(adversary, game)
        if winner == player.player_turn_id:
            score += 1
    return score
