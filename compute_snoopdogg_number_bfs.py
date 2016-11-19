#!/usr/bin/python2

# This script computes every artist's Snoop Dogg Number (and shortest path to Snoop Dogg) by
# performing a breadth-first traversal and computing the results in a single pass of the vertices.
# This method can be applied to the graph because it is unweighted. This script is O(V + E).
# I expect it to run in linear time for my purposes because the music collaboration graphs I use
# are sparse and will never come close to being fully connected. This script took 20 seconds to
# run on an i7-6700k.

import psycopg2
import networkx as nx

# Connect to the MusicBrainz database and load graph from disk
connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
cursor = connection.cursor()
graph = nx.read_gexf("graph/graph.gexf")

# Prepare the database
cursor.execute("DROP TABLE IF EXISTS snoopdogg_number_bfs;")
cursor.execute("""
    CREATE TABLE snoopdogg_number_bfs (
        artist   TEXT    NOT NULL,
        distance INTEGER NOT NULL,
        path     TEXT    NOT NULL,
        PRIMARY KEY(artist)
    );
""")

# Initialize dictionary with the Snoop Dogg as the base case
sdn = {"Snoop Dogg" : (0, ["Snoop Dogg"])}

# Traverse the graph breadth-first and compute every artist's Snoop Dogg Number in O(V + E)
for edge in nx.bfs_edges(graph, "Snoop Dogg"):
   parent = edge[0]
   child = edge[1]
   dist_to_snoopdogg = sdn[parent][0] + 1
   path_to_snoopdogg = sdn[parent][1] + [child]
   sdn[child] = (dist_to_snoopdogg, path_to_snoopdogg)

# Insert the data via one long query - this is an order of magnitude faster than one query per row
data_string = ','.join(cursor.mogrify('(%s,%s,%s)', (artist, sdn[artist][0], sdn[artist][1])) for artist in sdn) # mogrify requires python2
cursor.execute('INSERT INTO snoopdogg_number_bfs VALUES ' + data_string)

# Apply all changes to the database
connection.commit()
connection.close()
print("Done!")
