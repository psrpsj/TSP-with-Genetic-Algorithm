from TSP_model.geneset import GeneSet

class TSP_basic():
    def __init__(self, geneset : GeneSet):
        self.geneset = geneset
    
    def introduce_new_gene(self, save_rate):
        self.geneset.gene_set.sort()
        save_index = int(len(self.geneset) * save_rate)
        for i in range(save_index, len(self.geneset)):
            self.geneset.set_random_gene(i)
