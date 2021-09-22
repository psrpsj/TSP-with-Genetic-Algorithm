import random
from TSP_model.geneset import GeneSet

class Genetic_Algorithm():
    def __init__(self, geneset : GeneSet):
        self.geneset = geneset
    
    def introduce_new_gene(self, save_rate):
        """ Put new genes in gene set with specified number of saved genes

        Args:
            save_rate (float): the decimal rate of how many genes will be saved
        """
        self.geneset.gene_set.sort()
        save_index = int(len(self.geneset) * save_rate)
        for i in range(save_index, len(self.geneset)):
            self.geneset.set_random_gene(i)

    # adopted from https://www.koreascience.or.kr/article/CFKO200533239321725.pdf
    def breed(parent1, parent2):
        # save start node
        start = parent1[0]
        
        # remove start node from parents 
        parent1 = parent1[1:-1]
        parent2 = parent2[1:-1]

        # select random index
        point1 = random.randint(0, len(parent1) -1)
        point2 = random.randint(0, len(parent1) -1)

        while point1 == point2:
            point2 = random.randint(0, len(parent1) -1)

        start_point = min(point1, point2)
        end_point = max(point1, point2)

        # create offspring
        # offspring1 would have node from parent2 while 
        # offspring2 would have node from parent1
        offs1_mid = parent2[start_point : end_point]
        offs2_mid = parent1[start_point : end_point]

        # remove redundant node in each parent and offspring
        parent1_fixed = [node for node in parent1 if node not in offs1_mid]
        parent2_fixed = [node for node in parent2 if node not in offs2_mid]

        offspring1 = [start] + parent1_fixed[-start_point:] + offs1_mid + parent1_fixed[:len(parent1) - end_point] + [start]
        offspring2 = [start] + parent2_fixed[-start_point:] + offs2_mid + parent2_fixed[:len(parent2) - end_point] + [start]

        return offspring1, offspring2

    







