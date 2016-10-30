#!/usr/bin/python3

import psycopg2

connection = psycopg2.connect(database="musicbrainz", user="musicbrainz", password="", host="musicbrainz", port="5432")
print("Database opened successfully")

cursor = connection.cursor()
cursor.execute("""
        SELECT *
        FROM artist
        LIMIT 10;
""")

rows = cursor.fetchall()
for row in rows:
    print(row)

connection.close()
print("Done!")
