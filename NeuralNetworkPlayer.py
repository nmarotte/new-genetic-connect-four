import numpy as np

class NeuralNetworkPlayer:
    CHROMOSOME_LENGTH = None
    pass

    @staticmethod
    def reproduce(parents):
        children = [NeuralNetworkPlayer(), NeuralNetworkPlayer()]
        parent_a, parent_b = parents
        
        chromosomes_a, chromosomes_b = NeuralNetworkPlayer.interlace_chromosomes(parent_a, parent_b)

            children[0].neural_network.setWeights(i, new_chromosomes1)
            children[1].neural_network.setWeights(i, new_chromosomes2)
        return children

    @staticmethod
    def interlace_chromosomes(parent_a, parent_b):
        for i in range(len(parent_a.neural_network.weights)):
            split_point = np.random.randint(0, NeuralNetworkPlayer.CHROMOSOME_LENGTH)
            shape = parent_a.neural_network.weights[i].shape
    
            chromosomes1 = parent_a.neural_network.weights[i].flatten()
            chromosomes2 = parent_b.neural_network.weights[i].flatten()
    
            new_chromosomes1 = np.array(
                np.concatenate((chromosomes1[:split_point], chromosomes2[split_point:]))).reshape(shape)
            new_chromosomes2 = np.array(
                np.concatenate((chromosomes2[:split_point], chromosomes1[split_point:]))).reshape(shape)