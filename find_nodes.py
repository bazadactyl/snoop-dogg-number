#!/usr/bin/python3

import psycopg2

connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
cursor = connection.cursor()
print("Database opened successfully")

# Delete the old edges table
cursor.execute("""
    DROP TABLE IF EXISTS nodes;
""")

# Create new edges table
cursor.execute("""
    CREATE TABLE nodes (
        artist TEXT NOT NULL,
        PRIMARY KEY(artist)
    );
""")

# Find edges via artist credit and populate the edges table
query = open("sql/find_nodes.sql").read()
cursor.execute(query)

# Commit the changes
connection.commit()
connection.close()
print("Done!")
