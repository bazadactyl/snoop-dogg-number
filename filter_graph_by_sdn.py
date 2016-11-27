#!/usr/bin/python2

# TODO: Add description.

import psycopg2
import networkx as nx

# TODO: Create a class for storing artists' SDN and path to avoid doing this.
SDN = 0
PATH = 1

# Load graph from disk
graph = nx.read_gexf("graph/sdn-unweighted.gexf")

# Initialize dictionary with the Snoop Dogg as the base case
artists = {"Snoop Dogg" : (0, ["Snoop Dogg"])}

# Traverse the graph breadth-first and compute every artist's Snoop Dogg Number in O(V + E)
for edge in nx.bfs_edges(graph, "Snoop Dogg"):
   parent = edge[0]
   child = edge[1]
   dist_to_snoopdogg = artists[parent][SDN] + 1
   path_to_snoopdogg = artists[parent][PATH] + [child]
   artists[child] = (dist_to_snoopdogg, path_to_snoopdogg)

# Remove artists far from Snoop Dogg and save a separate graph for each iteration
# TODO: Can I use comprehensions to simplify these loops?
for sdn in [5, 4, 3, 2, 1]:
   distant_artists = []
   for a in artists:
      if artists[a][SDN] > sdn:
         distant_artists.append(a)

   for a in distant_artists:
      del artists[a]
      graph.remove_node(a)

   filename = "graph/sdn-" + str(sdn) + ".gexf"
   nx.write_gexf(graph, filename)
   print("Wrote graph of artists with SDN of " + sdn + " or less at " + filename)
   print(nx.info(graph))
