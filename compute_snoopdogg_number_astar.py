#!/usr/bin/python3

# This script computes every artist's Snoop Dogg Number by individually computing the shortest path
# between Snoop Dogg and every other artist in the graph. As the name of this file suggests, I am
# (naively) using the A-star algorithm implemented in the NetworkX library.
#
# As you might guess, this script is very, very slow. It took 15 hours to run on an i7-6700k despite
# being multi-threaded. Check out compute_snoopdogg_number_bfs.py for a quicker script that took a
# mere 20 seconds to accomplish the same thing on the same machine.

import psycopg2
import networkx as nx
import math
import multiprocessing

def split_tasks(num_tasks, num_processes):
    tasks = []
    tasks_per_process = math.ceil(num_tasks / num_processes)
    for i in range(0, num_processes):
        lo = (i * tasks_per_process) + 1
        hi = (i+1) * tasks_per_process
        hi = min(hi, num_tasks) # Avoid going beyond the last task
        task_range = (lo, hi)
        tasks.append(task_range)
    return tasks

def prepare_database():
    # Connect to the MusicBrainz database
    connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
    cursor = connection.cursor()
    print("Database preparation started")

    # Re-create the table
    cursor.execute("DROP TABLE IF EXISTS snoopdogg_number_astar;")
    cursor.execute("""
        CREATE TABLE snoopdogg_number_astar (
            artist   TEXT    NOT NULL,
            distance INTEGER NOT NULL,
            PRIMARY KEY(artist)
        );
    """)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()
    print("Database preparation finished")

def get_num_artists():
    # Connect to the MusicBrainz database
    connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
    cursor = connection.cursor()

    # Get number of nodes that needs to be processed
    cursor.execute("SELECT count(*) FROM nodes;")
    num_rows = cursor.fetchone()[0]

    # Close the connection
    connection.close()
    return num_rows

# Worker processes each run an instance of this function
def aggregate_sdn(range):
    # Get name and PID of this worker process
    pname = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid

    # Connect to the MusicBrainz database
    connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
    cursor = connection.cursor()
    print(pname + ": Database opened successfully")

    # Load graph from disk
    graph = nx.read_gml("graph/graph.gml")

    # Fetch the artists this worker process is responsible for
    first_row = range[0]
    last_row = range[1]
    num_rows = last_row - first_row + 1
    cursor.execute("SELECT artist FROM nodes LIMIT %s OFFSET %s;", (num_rows, first_row-1))

    # Populate the table with Snoop Dogg numbers for the rows assigned to this worker
    artists = cursor.fetchall()
    for artist in artists:
        artist_name = artist[0]
        try:
            sdn = nx.astar_path_length(graph, 'Snoop Dogg', artist_name)
        except nx.NetworkXNoPath:
            sdn = 0
        print(pname + ": " + artist_name + " " + str(sdn))
        cursor.execute("INSERT INTO snoopdogg_number VALUES (%s, %s)", (artist_name, sdn))

    # Apply changes from this worker to the database
    connection.commit()
    connection.close()
    print(pname + ": Done!")

# Main process
if __name__ == '__main__':
    prepare_database()
    num_tasks = get_num_artists()
    num_processes = 4
    tasks = split_tasks(num_tasks, num_processes)

    # Spawn worker processes
    pool = multiprocessing.Pool(num_processes)
    pool.map(aggregate_sdn, tasks)
