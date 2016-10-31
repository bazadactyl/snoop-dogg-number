#!/usr/bin/python3

import psycopg2

connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
cursor = connection.cursor()
print("Database opened successfully")

# Sample query
cursor.execute("""
        SELECT *
        FROM artist
        LIMIT 10;
""")

# Print out the table
rows = cursor.fetchall()
for row in rows:
    print(row)

# Commit the changes
connection.commit()
connection.close()
print("Done!")
