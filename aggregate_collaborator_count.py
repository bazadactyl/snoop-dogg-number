#!/usr/bin/python3

import psycopg2

connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
cursor = connection.cursor()
print("Database opened successfully")

# Delete the old collaborator_count table
cursor.execute("""
    DROP TABLE IF EXISTS collaborator_count;
""")

# Create new collaborator_count table
cursor.execute("""
    CREATE TABLE collaborator_count (
        artist TEXT NOT NULL,
        count INTEGER NOT NULL,
        PRIMARY KEY(artist)
    );
""")

# Populate the collaborator_count table
query = open("aggregate_collaborator_count.sql").read()
cursor.execute(query)

# Commit the changes
connection.commit()
connection.close()
print("Done!")
