import os
import random
from tqdm import tqdm

class Gene():
    def __init__ (self, start_node, path_data):
        """Initialize gene 

        Args:
            start_node (int): number of node that gene should start
            path_data (list): list of matrix representation contains cost of node to other node
        """
        self.path_data = path_data
        self.start_node = start_node
        self.gene = [self.start_node]

        while len(self.gene) < len(self.path_data):
            candidate = random.randint(1, len(self.path_data))
            # append candidate not in gene
            if candidate not in self.gene:
                self.gene.append(candidate)
            # add start at the end
        self.gene.append(self.start_node)

    def calculate_cost(self):
        """Calculate cost of gene

        Returns:
            cost (int): cost of gene
        """
        cost = 0
        for i in range (len(self.gene) -1):
            cost += self.path_data[self.gene[i] - 1][self.gene[i+1] -1]
        return cost

    def __eq__(self, other):
        return self.calculate_cost() == other.calculate_cost()
    
    def __lt__(self,other):
        return self.calculate_cost() < other.calculate_cost()
    

class GeneSet():
    """
    list of gene 
    """
    def __init__ (self, data_path, num_gene, start_node):
        """Initialize the Geneset with number of gene specified

        Args:
            data_path (str): name of dataset in dataset folder
            num_gene (int): number of gene in gene set
            start_node (int): number of node that each gene should start
        """
        self.num_gene = num_gene
        self.start_node = start_node
        self.data_path = os.path.join("dataset", data_path)
        self.path_file = open(self.data_path, 'r')
        self.path_data = [[int(n) for n in line.split()] for line in self.path_file]
        print(self.path_data)
        self.gene_set = []

        for i in tqdm(range(self.num_gene)):
            self.gene_set.append(Gene(self.start_node, self.path_data).gene)
    
    def __len__(self):
        return len(self.gene_set)

    def __repr__(self):
        represent = ""
        for gene in self.gene_set:
            represent += str(gene) + "\n"
        return represent

