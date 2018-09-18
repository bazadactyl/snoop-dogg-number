# The Snoop Dogg Number

## Project Objective

Searching for the Erdős of the music world through collaboration graphs.

## About

I'm using the MusicBrainz database to investigate collaborative relationships between musicians.

Mathematicians compute [Erdős numbers](https://en.wikipedia.org/wiki/Erd%C5%91s_number) to measure the distance between themselves and the most prolific mathematician yet, Paul Erdős. Imagine creating a large graph where each mathematician with a published paper is a node. Now, add an edge for every time a pair of mathematicians collaborated on a paper. By using a shortest path algorithm on this graph for two mathematicians, Alice and Bob, we can compute the distance between them in the collaboration graph.

One of the questions I want to answer in this project is: who is the Erdős of the music world? My light-hearted hypothesis says it's Snoop Dogg, who seems to collaborate with musicians from many different genres. Perhaps his cousin Nate Dogg would have won had his untimely death not happened.

Another objective is to create a web interface to the collaboration graphs I'm generating. Users could traverse the graph and explore the relationships between musicians. Users would also be able to compute the distance between any two musicians.

Check out [this slideshow](https://docs.google.com/presentation/d/1XPBdZAUYaJDz9-o_QmASU8lSTGbGSa0s2BBSBlFMKFM/edit?usp=sharing) I used to present my project to my class.

## Recent Results

After running a layout algorithm on the collaboration graph, followed by a community finding algorithm, I was able to visualize the community Snoop Dogg belongs to.

![Alt text](viz/communities_yifanhu_6.png?raw=true "Snoop Dogg's community")

Using the "artist credit" proved to be the easiest way of finding collaboration edges between artists. However, the results are incorrectly skewed in favor of famous deceased composers. See `find_edges_via_credit.sql` to see the query that generated the edges that led to these results.

![Alt text](collaborator_count.png?raw=true "Collaborator counts based on the artist credit method of finding edges")

Things are looking good for this project's titular artist.
