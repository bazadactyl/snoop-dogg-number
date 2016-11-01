#!/usr/bin/python3

import psycopg2
import networkx as nx
import pickle
import json
from networkx.readwrite import json_graph

def write_json_nodelink(graph):
    node_link_data = json_graph.node_link_data(graph)
    with open('graph/graph.nodelink.json', 'w') as outfile:
        json.dump(node_link_data, outfile, indent=2)

def write_json_adjacency(graph):
    adjacency_data = json_graph.adjacency_data(graph)
    with open('graph/graph.adjacency.json', 'w') as outfile:
        json.dump(adjacency_data, outfile, indent=2)

def write_other_formats(graph):
    nx.write_adjlist(graph, "graph/graph.adjlist", delimiter='||')
    nx.write_multiline_adjlist(graph, "graph/graph.multi.adjlist", delimiter='||')
    nx.write_edgelist(graph, "graph/graph.edgelist", delimiter='||')
    nx.write_gexf(graph, "graph/graph.gexf")
    nx.write_gml(graph, "graph/graph.gml")
    nx.write_gml(graph, "graph/graph.gml.gz")
    nx.write_gpickle(graph, "graph/graph.gpickle")
    nx.write_graphml(graph, "graph/graph.graphml")
    nx.write_yaml(graph, "graph/graph.yaml")
    # nx.write_graph6(graph, "graph/graph.graph6") # https://github.com/networkx/networkx/issues/2295
    nx.write_sparse6(graph, "graph/graph.sparse6")
    nx.write_pajek(graph, "graph/graph.pajek")

# Connect to the MusicBrainz database
connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
cursor = connection.cursor()
print("Database opened successfully")

# Initialize the graph
graph = nx.Graph()

# Fetch all edges from the database
cursor.execute('''
    DECLARE db_cursor BINARY CURSOR FOR
        SELECT collaborator1, collaborator2 FROM edges;
''')

# Incrementally populate the graph with edges
while True:
    cursor.execute("FETCH 10000 FROM db_cursor")
    edges = cursor.fetchall()
    if not edges:
        break
    else:
        graph.add_edges_from(edges)

# Write the graph to disk in several formats
write_json_nodelink(graph)
write_json_adjacency(graph)
write_other_formats(graph)

# Close the connection
connection.close()
print("Done!")
