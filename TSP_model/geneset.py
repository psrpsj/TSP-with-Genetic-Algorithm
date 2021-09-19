import os
import random

class GeneSet():
    def __init__ (self, data_path, num_gene, start_node):
        self.data_path = os.path.join("dataset", data_path)
        self.num_gene = num_gene
        self.path_file = open(self.data_path, 'r')
        self.path_data = [[int(n) for n in line.split()] for line in self.path_file]
        self.gene_set = []

        while len(self.gene_set) < self.num_gene:
            gene = [start_node]
            while len(gene) != len(self.path_data):
                candidate = random.randint(1, len(self.path_data))
                # append candidate not in gene
                if candidate not in gene:
                    gene.append(candidate)
            # add start at the end
            gene.append(start_node)
            self.gene_set.append(gene)
        

