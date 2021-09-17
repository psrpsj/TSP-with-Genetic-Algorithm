import os
import random


#### Prepare ####

def load_data(file_name):
    """ Function to load data in dataset folder

    Args:
        file_name (string): the file name in the dataset folder

    Returns:
        path_data (list): distance matrix in list type
    """
    path = os.path.join("dataset", file_name)
    path_file = open(path, 'r')
    path_data = [[int(n) for n in line.split()] for line in path_file]
    return path_data


#### TSP ####

def create_gene(graph, start):
    gene = [start]
    while len(gene) != len(graph):
        


