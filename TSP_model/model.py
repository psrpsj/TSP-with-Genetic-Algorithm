import random
from geneset import Gene, GeneSet

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
    def breed(self, parent1 : Gene, parent2 : Gene):
        """ Create 2 offspring genes from 2 parents genes

        Args:
            parent1 (Gene): parent gene to produce offspring
            parent2 (Gene): parent gene to produce offspring

        Returns:
            offspring1, offspring2: offspring produced from parents genes
        """
        # save start node
        start = parent1.gene[0]
        
        # remove start node from parents 
        parent1_node = parent1.gene[1:-1]
        parent2_node = parent2.gene[1:-1]

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
        parent1_fixed = [node for node in parent1_node if node not in offs1_mid]
        parent2_fixed = [node for node in parent2_node if node not in offs2_mid]

        offspring1 = [start] + parent1_fixed[:start_point] + offs1_mid + parent1_fixed[-(len(parent1) - end_point)] + [start]
        offspring2 = [start] + parent2_fixed[:start_point] + offs2_mid + parent2_fixed[-(len(parent2) - end_point)] + [start]

        return offspring1, offspring2

    def mutation(self, mutation_rate):
        """ Gene to be changed by mutation

        Args:
            mutation_rate (float):  percentage in decimal that gene would be mutated
        """
        num_mutate = int(mutation_rate * len(self.geneset))

        already_mutated = []
        for _ in range(0, num_mutate):
            index = random.randint(0, len(self.geneset) -1)
            while index in already_mutated:
                index = random.randint(0, len(self.geneset) -1)
            
            index1 = random.randint(1, len(self.geneset.get_gene(index)) -2)
            index2 = random.randint(1, len(self.geneset.get_gene(index)) -2)
            
            while index1 == index2:
                index2 = random.randint(1, len(self.geneset.get_gene(index)) -2)
            
            temp = self.geneset.get_gene(index).gene[index1]
            self.geneset.get_gene(index).gene[index1] = self.geneset.get_gene(index).gene[index2]
            self.geneset.get_gene(index).gene[index2] = temp
            already_mutated.append(index)
    
    def train(self, num_generation, new_gene_rate, mutation_rate):
        
        min_route = self.geneset.get_gene(0)
        min_cost = self.geneset.get_gene(0).calculate_cost()
        print("Initial mininum route : ", min_route)
        print("Initial minimum cost : ", min_cost)

        for number in range(1, num_generation + 1):
            # introduce new gene in geneset
            self.introduce_new_gene(new_gene_rate)
            
            # breed procedure
            breed1 = random.randint(0, len(self.geneset) -1)
            breed2 = random.randint(0, len(self.geneset) -1)
            
            while breed1 == breed2:
                breed2 = random.randint(0, len(self.geneset) -1)
            
            offspring1, offspring2 = self.breed(self.geneset.get_gene(breed1), self.geneset.get_gene(breed2))
            self.geneset.set_gene(breed1, offspring1)
            self.geneset.set_gene(breed2, offspring2)

            # mutation
            self.mutation(mutation_rate)

            # sort and print current-generation min cost and route
            self.geneset.gene_set.sort()

            tmp_min_route = self.geneset.get_gene(0)
            tmp_min_cost = self.geneset.get_gene(0).calculate_cost()

            if tmp_min_cost < min_cost:
                min_route = tmp_min_route
                min_cost = tmp_min_cost
                
            print("Generation " + str(number) + " minimum route : ", min_route)
            print("Generation " + str(number) + " minimum cost : ", min_cost)

        print("Final minimum route : ", min_route)
        print("Final minimum cost : ", min_cost)