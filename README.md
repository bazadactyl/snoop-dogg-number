# The Snoop Dogg Number

## Project Objective

Searching for the Erdős of the music world through collaboration graphs.

## About

Check out [this slideshow](https://docs.google.com/presentation/d/15aCywqfPQVtDyaG_jlWs1wb7m9kY4JCkGDMM6KbOudo/edit?usp=sharing) for a basic idea of my goals for the project and my progress so far.

## Recent Results

Using the "artist credit" proved to be the easiest way of finding collaboration edges between artists. However, the results are incorrectly skewed in favor of famous deceased composers. See `find_edges_via_credit.sql` to see the query that generated the edges that led to these results.

![Alt text](collaborator_count.png?raw=true "Collaborator counts based on the artist credit method of finding edges")

Things are looking good for this project's titular artist.
