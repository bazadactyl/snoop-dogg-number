#!/usr/bin/python3

# This script performs some simple benchmarking for some of the shortest path algorithm
# implementations provided by NetworkX. I was mostly interested in comparing the standard
# deviation between the different algorithms to see how consistent they performed.

import networkx as nx
import multiprocessing
import random
import time
import numpy as np
import math

def random_pairs(elements, num_pairs):
   num_samples = num_pairs * 2
   samples = random.sample(elements, num_samples)
   pairs = []
   for i in range(0, num_samples, 2):
      pair = (samples[i], samples[i+1])
      pairs.append(pair)
   return pairs

def print_statistics(numbers, label):
   total = np.sum(numbers)
   mean = np.mean(numbers)
   median = np.median(numbers)
   std = np.std(numbers)
   var = np.var(numbers)
   statistics = "({0}) Total = {1} Mean = {2}, Median = {3}, Standard Deviation = {4}, Variance = {5}".format(label, total, mean, median, std, var)
   print(statistics)

def benchmark(shortest_path, graph, pairs):
   compute_times = []
   for pair in pairs:
      start = time.time()
      try:
         path = shortest_path(graph, pair[0], pair[1])
         distance = len(path) - 1
      except nx.NetworkXNoPath:
         path = []
         distance = math.inf
      end = time.time()
      compute_times.append(end - start)
   print_statistics(compute_times, shortest_path.__name__)

# Main process
if __name__ == '__main__':
   # Load graph from disk and generate random test data
   graph = nx.read_gexf("graph/graph.gexf")
   artists = nx.nodes(graph)
   num_artists = nx.number_of_nodes(graph)
   test_data = random_pairs(artists, 10000)

   # Select algorithms to benchmark
   algorithms = [nx.astar_path, nx.dijkstra_path, nx.shortest_path]
   num_processes = len(algorithms)

   # Spawn worker processes then wait for them to finish
   pool = multiprocessing.Pool(num_processes)
   for algorithm in algorithms:
      pool.apply_async(benchmark, (algorithm, graph, test_data))
   pool.close()
   pool.join()
