#!/usr/bin/python3

import psycopg2
import networkx as nx
import pickle
import json
from networkx.readwrite import json_graph

def write_json_nodelink(graph):
    node_link_data = json_graph.node_link_data(graph)
    with open('graph/sdn-weighted.nodelink.json', 'w') as outfile:
        json.dump(node_link_data, outfile, indent=2)

def write_json_adjacency(graph):
    adjacency_data = json_graph.adjacency_data(graph)
    with open('graph/sdn-weighted.adjacency.json', 'w') as outfile:
        json.dump(adjacency_data, outfile, indent=2)

def write_common_formats(graph):
    nx.write_gexf(graph, "graph/sdn-weighted.gexf")
    nx.write_gml(graph, "graph/sdn-weighted.gml")
    nx.write_graphml(graph, "graph/sdn-weighted.graphml")

def write_other_formats(graph):
    nx.write_adjlist(graph, "graph/sdn-weighted.adjlist", delimiter='||')
    nx.write_multiline_adjlist(graph, "graph/sdn-weighted.multi.adjlist", delimiter='||')
    nx.write_edgelist(graph, "graph/sdn-weighted.edgelist", delimiter='||')
    nx.write_gpickle(graph, "graph/sdn-weighted.gpickle")
    nx.write_yaml(graph, "graph/sdn-weighted.yaml")
    # nx.write_graph6(graph, "graph/sdn-weighted.graph6") # https://github.com/networkx/networkx/issues/2295
    nx.write_sparse6(graph, "graph/sdn-weighted.sparse6")
    nx.write_pajek(graph, "graph/sdn-weighted.pajek")

# Connect to the MusicBrainz database
connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
cursor = connection.cursor()
print("Database opened successfully")

# Create a cursor in the database
cursor.execute('''
    DECLARE db_cursor CURSOR FOR
        SELECT collaborator1, collaborator2, num_collabs FROM weighted_edges;
''')

# Initialize the undirected graph
graph = nx.Graph()

# Incrementally populate the graph with edges using the database cursor
while True:
    cursor.execute("FETCH 10000 FROM db_cursor")
    edges = cursor.fetchall()
    if not edges:
        break
    for e in edges:
        graph.add_edge(e[0], e[1], weight=e[2])
    print(nx.info(graph))

# Write the graph to disk
write_common_formats(graph)

# Close the connection
connection.close()
print("Done!")
