import pygame

from NeuralNetwork import NeuralNetwork, NeuralNetworkPlayer
from MinMax import MinimaxPlayer
import numpy as np
from game import Connect4Game, Connect4Viewer, SQUARE_SIZE

INPUT_LAYER = 126
OUTPUT_LAYER = 7
INTERMEDIATE_LAYERS = (126, 126)


class Generation:

    def __init__(self, nb_players, nb_generations, nb_games):
        self.nb_players = nb_players
        self.nb_generations = nb_generations
        self.nb_games = nb_games
        self.players = [NeuralNetworkPlayer(NeuralNetwork(INPUT_LAYER, OUTPUT_LAYER, INTERMEDIATE_LAYERS)) for _ in
                        range(self.nb_players)]
        self.tournament()

    def tournament(self):
        for gen in range(self.nb_generations):
            """
            for game in range(self.nb_games):
                for i in range(self.nb_players):
                    for j in range(self.nb_players):
                        if i != j:
                            winner = self.play(self.players[i], self.players[j], game = Connect4Game())
                            if winner == 0:
                                self.players[i].addScore(0.25)
                                self.players[j].addScore(0.25)
                            elif winner == 1:
                                self.players[i].addScore(1)
                            else:
                                self.players[j].addScore(1)
            """
            if gen%10 == 0: print(gen)
            self.nextGen()

    def play(self, player1, player2, game):
        flag = False
        if game.get_turn() == 2:
            flag = True
        playing = True
        while playing:
            game.place(player1.chooseAction(game.get_board()))
            winner = game.get_win()
            if winner is None:
                #game.place(player2.chooseAction(game.get_board()))
                game.place(player2.chooseAction()[0])
                winner = game.get_win()
                if winner is not None:
                    playing = False
            else:
                playing = False

        if winner != 0 and flag:
            winner = 3 - winner
        return winner

    """
    def fitness(self):
        scores = []
        total = sum([p.getScore() for p in self.players])
        for player in self.players:
            scores.append(player.getScore() / total)
        return scores
    """

    def fitness(self):
        scores = []
        for player in self.players:
            player_score = 1
            for i in range(10):
                game = Connect4Game()
                winner = self.play(player, MinimaxPlayer(3 - game.get_turn(), game.board), game)
                if winner == 0:
                    player_score += 50
                elif winner == 1:
                    player_score += 100
            scores.append(player_score)
        total = sum(scores)
        for i in range(len(scores)):
            scores[i] = scores[i]/total
        return scores

    def nextGen(self):
        prob = self.fitness()
        newGen = np.random.choice(self.players, size=len(self.players) // 2, replace=False, p=prob)
        while len(newGen) < len(self.players):
            parents = np.random.choice(self.players, size=2, replace=False, p=prob)
            children = self.reproduce(parents)
            newGen = np.append(newGen, children)
        for player in newGen:
            player.resetScore()
        self.players = newGen

    def reproduce(self, parents):
        children = [NeuralNetworkPlayer(NeuralNetwork(INPUT_LAYER, OUTPUT_LAYER, INTERMEDIATE_LAYERS)),
                    NeuralNetworkPlayer(NeuralNetwork(INPUT_LAYER, OUTPUT_LAYER, INTERMEDIATE_LAYERS))]
        for i in range(len(parents[0].neural_network.weights)):
            shape = parents[0].neural_network.weights[i].shape
            chromosomes1 = parents[0].neural_network.weights[i].flatten()
            chromosomes2 = parents[1].neural_network.weights[i].flatten()
            split_point = np.random.randint(0, len(chromosomes1))
            new_chromosomes1 = np.array(
                np.concatenate((chromosomes1[:split_point], chromosomes2[split_point:]))).reshape(shape)
            new_chromosomes2 = np.array(
                np.concatenate((chromosomes2[:split_point], chromosomes1[split_point:]))).reshape(shape)
            children[0].neural_network.setWeights(i, new_chromosomes1)
            children[1].neural_network.setWeights(i, new_chromosomes2)
        return children

"""
for j in range(10):
    gen = Generation(20, 100, 1)
    x = 0

    for i in range(1000):

        game = Connect4Game()
        game.reset_game()

        player1 = gen.players[0]
        player2 = MinimaxPlayer(3 - game.get_turn(), game.board)

        playing = True
        while playing:
            action = player1.chooseAction(game.get_board())
            game.place(action)
            winner = game.get_win()
            if winner is None:
                game.place(player2.chooseAction()[0])
                winner = game.get_win()
                if winner is not None:
                    playing = False
            else:
                playing = False
        if winner == 0:
            pass
        elif winner == player2.player:
            pass
        else:
            x += 1

    print("neural net won {0} times".format(x))



"""
gen = Generation(20, 100, 1)
player = gen.players[0]
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
                player_a_choice = player.chooseAction(game.get_board())
                game.place(player_a_choice)
            else:
                game.reset_game()
