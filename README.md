# The Snoop Dogg Number

## About

I'm using the MusicBrainz database to investigate collaborative relationships between musicians.

Mathematicians compute [Erdős numbers](https://en.wikipedia.org/wiki/Erd%C5%91s_number) to measure the distance between themselves and the most prolific mathematician yet, Paul Erdős. Imagine creating a large graph where each mathematician with a published paper is a node. Now, add an edge for every time a pair of mathematicians collaborated on a paper. By using a shortest path algorithm on this graph for two mathematicians, Alice and Bob, we can compute the distance between them in the collaboration graph.

One of the questions I want to answer in this project is: who is the Erdős of the music world? My light-hearted hypothesis says it's Snoop Dogg, who seems to collaborate with musicians from many different genres. Perhaps his cousin Nate Dogg would have won had his untimely death not happened.

Another objective is to create a web interface to the collaboration graphs I'm generating. Users could traverse the graph and explore the relationships between musicians. Users would also be able to compute the distance between any two musicians.

## Results

Surprisingly, I was right! Snoop Dogg is indeed the most collaborative music artist alive. In [this screenshot](collaborator_count.png) you'll see how many collaborators the top artists have. Putting aside dead classical composers (Bach, Mozart, and Beethoven) who have a high collaborator count due to orchestras playing their music in recent decades, Snoop is miles ahead of any of his contemporaries with 803 collaborators! Behind him in second place is Busta Rhymes with 549 and Lil Wayne with 548.

After running a layout algorithm on the collaboration graph, followed by a community finding algorithm, I was able to visualize the [community Snoop Dogg belongs to](presentation/communities_yifanhu_6.png). Interestingly, Busta and Wayne are in a [different, and larger community](presentation/communities_yifanhu_1.png).

Check out the [slide deck](presentation/presentation.pdf) I presented to the class. You'll see the work I did to analyze the MusicBrainz database and visualize musical communities.

![Alt text](viz/communities_yifanhu_6.png?raw=true "Snoop Dogg's community")
