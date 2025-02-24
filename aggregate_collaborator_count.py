#!/usr/bin/python3

import psycopg2

# Connect to the MusicBrainz database
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
query = open("sql/aggregate_collaborator_count.sql").read()
cursor.execute(query)

# Apply the changes to the database
connection.commit()
connection.close()
print("Done!")
