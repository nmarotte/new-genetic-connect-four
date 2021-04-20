import random

import pygame

from GeneticLayers import Agent
from Old.game import Connect4Game, SQUARE_SIZE, Connect4Viewer
import numpy as np


def play_human(alex: Agent):
    game = Connect4Game()
    game.reset_game()
    view = Connect4Viewer(game=game)
    view.initialize()
    running = True
    while running:
        for i, event in enumerate(pygame.event.get()):
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if game.get_win() is None:
                    placement = game.place(pygame.mouse.get_pos()[0] // SQUARE_SIZE)
                    if placement is None:  # Still player's turn if placement fails
                        continue
                    if game.get_win() is not None:
                        game.reset_game()
                    player_a_choice = alex.get_choice(game.board, show=True)
                    game.place(player_a_choice)
                else:
                    game.reset_game()


def play_one_game(alex: Agent, bob: Agent) -> Agent:
    game = Connect4Game()
    game.reset_game()

    winner = game.get_win()
    if random.randint(0,1):  # Pick first player at random
        alex, bob = bob, alex

    while winner is None:
        game.place(alex.get_choice(game.board))
        winner = game.get_win()
        if winner is not None:
            break

        game.place(bob.get_choice(game.board))
        winner = game.get_win()

    return alex if winner == 1 else bob if winner == 2 else None


def generation_tournament(players: list[Agent]):
    # Training phase
    for _ in range(200):
        alex, bob = np.random.choice(players, size=2, replace=False)
        winner = play_one_game(alex, bob)
        winner.backpropagation()

    # Competition phase
    for i in range(len(players) - 1):
        for j in range(i + 1, len(players)):
            alex, bob = players[i], players[j]
            winner = play_one_game(alex, bob)
            alex.nb_played += 1
            bob.nb_played += 1
            if winner is not None:
                winner.score += 1 / winner.moves_of_game
                winner.backpropagation()
    players.sort(key=lambda p: p.score, reverse=True)
    return players


def mix_shapes(agents: list[Agent]):
    return np.random.choice(agents).shapes


def generate_next_generation(players: list[Agent]):
    """
    Transform the current generation in the next one by keeping best, killing worst, and mixing others
    :param players: the sorted list by score of the players
    :return: next_generation: the next generation that depends on random and on the current generation
    """
    n = len(players)
    lef = 12.5  # Life Expectancy Factor (The higher the factor, the more agents survive from the generation to next

    nb_keep = int(n // lef)
    # Keep top LEF
    top = players[:nb_keep]
    # Keep bottom LEF
    bot = players[-nb_keep:]

    # Mix the rest
    players = players[nb_keep:-nb_keep]

    total_score = sum(p.score for p in players)
    generation_scores = [p.score / total_score for p in players]
    new_players = top + bot
    while len(new_players) < n:
        couple = np.random.choice(a=players, size=2, replace=False, p=generation_scores)
        new_players.append(Agent.mix_agents(couple))

    return new_players
