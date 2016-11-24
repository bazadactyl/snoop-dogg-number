#!/usr/bin/python3

import psycopg2

connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
cursor = connection.cursor()
print("Database opened successfully")

# Delete the old edges table
cursor.execute("""
    DROP TABLE IF EXISTS unweighted_edges;
""")

# Create new edges table
cursor.execute("""
    CREATE TABLE unweighted_edges (
        collaborator1 TEXT NOT NULL,
        collaborator2 TEXT NOT NULL,
        PRIMARY KEY(collaborator1, collaborator2)
    );
""")

# Find edges via artist credit and populate the edges table
query = open("sql/find_unweighted_edges_via_credit.sql").read()
cursor.execute(query)

# Apply the changes to the database
connection.commit()
connection.close()
print("Done!")
