from GeneticLayers import Agent
from game import Connect4Game


def play_one_game(alex: Agent, bob: Agent) -> Agent:
    game = Connect4Game()
    game.reset_game()

    winner = game.get_win()

    while winner is None:
        player_a_choice = alex.get_choice(game.board)
        game.place(player_a_choice)
        winner = game.get_win()
        if winner is not None:
            break

        player_b_choice = bob.get_choice(game.board)
        game.place(player_b_choice)
        winner = game.get_win()

    return alex if winner == 1 else bob if winner == 2 else None


def generation_tournament(players: list[Agent]):
    for i in range(len(players) - 1):
        for j in range(i + 1, len(players)):
            alex, bob = players[i], players[j]
            winner = play_one_game(alex, bob)
            alex.nb_played += 1
            bob.nb_played += 1
            winner.score += 1
    players.sort(key=lambda p: p.score, reverse=True)
    return players
