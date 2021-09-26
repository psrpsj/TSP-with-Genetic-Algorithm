import random
import argparse
from geneset import Gene, GeneSet

class Genetic_Algorithm():
    def __init__(self, geneset):
        self.geneset = geneset
    
    def introduce_new_gene(self, save_rate):
        """ Put new genes in gene set with specified number of saved genes

        Args:
            save_rate (float): the decimal rate of how many genes will be saved
        """
        self.geneset.sort()
        save_index = int(len(self.geneset) * save_rate)
        for i in range(save_index, len(self.geneset)):
            self.geneset.set_random_gene(i)

    # adopted from https://www.koreascience.or.kr/article/CFKO200533239321725.pdf
    def breed(self, parent1, parent2):
        """ Create 2 offspring genes from 2 parents genes

        Args:
            parent1 (Gene): parent gene to produce offspring
            parent2 (Gene): parent gene to produce offspring

        Returns:
            tuple: Two routes that would be offspring from two parents gene 
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
        offs1_mid = parent2_node[start_point : end_point]
        offs2_mid = parent1_node[start_point : end_point]

        # remove redundant node in each parent and offspring
        parent1_fixed = [node for node in parent1_node if node not in offs1_mid]
        parent2_fixed = [node for node in parent2_node if node not in offs2_mid]

        route1 = [start] + parent1_fixed[:start_point] + offs1_mid + parent1_fixed[start_point:] + [start]
        route2 = [start] + parent2_fixed[:start_point] + offs2_mid + parent2_fixed[start_point:] + [start]

        return route1, route2

    def select_breed_gene(self, selected_index):
        """Select gene from geneset using Roulette wheel Selection Algorithm

        Args:
            geneset (Geneset): Geneset to select genes

        Returns:
            tuple: Two genes randomly selected
        """

        mid_1 = int(len(self.geneset) * 0.3)
        mid_2 = int(len(self.geneset) * 0.7)

        tmp_list = self.geneset.gene_set[:mid_1] * 4 + self.geneset.gene_set[mid_1 : mid_2] * 3 + self.geneset.gene_set[mid_2:]

        # two indicies should not be already have been into breed process and two indicies should not equal 
        gene1_index = random.randint(0, len(tmp_list) - 1)
        while gene1_index in selected_index:
            gene1_index = random.randint(0, len(tmp_list) - 1)

        gene2_index = random.randint(0, len(tmp_list) - 1)
        while gene1_index == gene2_index and gene2_index not in selected_index:
            gene2_index = random.randint(0, len(tmp_list) - 1)
        
        selected_index += [gene1_index, gene2_index]
        
        return tmp_list[gene1_index], tmp_list[gene2_index]


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
    
    def train(self, num_generation, new_gene_rate, breed_time, mutation_rate):
        """ Find minimum route

        Args:
            num_generation (int): number of generation the algorithim will run
            new_gene_rate (float): rate to be use in introduce_new_gene process
            breed_time (int): number of breed should be run in each generation (should not be over the half of number of gene)
            mutation_rate (float): rate to be use in mutation process 
        """
        min_route = self.geneset.get_gene(0)
        min_cost = self.geneset.get_gene(0).calculate_cost()
        print("Initial mininum route : ", min_route)
        print("Initial minimum cost : ", min_cost)

        for number in range(1, num_generation + 1):
            # introduce new gene in geneset
            self.introduce_new_gene(new_gene_rate)
            
            # breed procedure
            breed_index = []
            for i in range (1, breed_time * 2 + 1, 2):
                breed1, breed2 = self.select_breed_gene(breed_index)
                breed_result1, breed_result2 = self.breed(breed1, breed2)
                self.geneset.set_gene_route(-i, breed_result1)
                self.geneset.set_gene_route(-i-1, breed_result2)


            # mutation
            self.mutation(mutation_rate)

            # sort and print current-generation min cost and route
            self.geneset.sort()

            tmp_min_route = self.geneset.get_gene(0)
            tmp_min_cost = self.geneset.get_gene(0).calculate_cost()

            if tmp_min_cost < min_cost:
                min_route = tmp_min_route
                min_cost = tmp_min_cost
                
            print("Generation " + str(number) + " minimum route : ", min_route)
            print("Generation " + str(number) + " minimum cost : ", min_cost)

        print("Final minimum route : ", min_route)
        print("Final minimum cost : ", min_cost)

        return min_cost

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # GeneSet arguments
    parser.add_argument('--dataset', type=str, default='att48_d.txt', help = 'dataset to use to find route (default: five_d.txt)')
    parser.add_argument('--population', type=int, default=100, help= 'number of genes in geneset (default: 10)')
    parser.add_argument('--startnode', type=int, default=1, help='number of node route should start and end (defalut: 1)')

    # GA arguments
    parser.add_argument('--generation', type=int, default=80, help='generation would GA run (defalut: 10)')
    parser.add_argument('--newgenerate', type=float, default=0.9, help= 'rate of new gene will be introduced in each generation (defalut: 0.2)')
    parser.add_argument("--breednumber", type=int, default=40, help='number of breed will occur in each generation (default: 4)')
    parser.add_argument('--mutationrate', type=float, default=0.1, help= 'rate of mutation will occur each generation (defalut: 0.1)')

    args = parser.parse_args()

    data = GeneSet(args.dataset, args.population, args.startnode)
    GA_test = Genetic_Algorithm(data)
    GA_test.train(args.generation, args.newgenerate, args.breednumber, args.mutationrate)