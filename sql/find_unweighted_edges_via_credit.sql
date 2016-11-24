-- This SQL query populates the edges table of collaboration edges between
-- artists simply based on "artist credit".
--
-- For example, the artist credit
--     "Kanye West feat. RZA, Jay-Z, Pusha T, Swizz Beatz & CyHi da Prynce"
-- contains six artists (and therefore 6 choose 2 = 15 edges) who have
-- collaborated on a recording.
--
-- This method of finding collaborations misses every collaborative edge between
-- members of a band because the band's artist credit only has the band's name,
-- without the names of the individual band members withoutcollborated with each
-- other. For example, the edge (John Lennon, Ringo Starr) will be missed because
-- their collaboration is credited simply as "The Beatles". Furthermore, the
-- results of this query incorrectly reports famous classical composers like
-- Tchaikovsky or Bach as prolific collaborators because many recent orchestras
-- have released albums where the credit includes a deceased composer.

WITH
nodes AS ( -- Each row of this table has a "collaboration" and one of its "collaborators"
    SELECT
        ac.name AS collaboration,
        acn.name AS collaborator
    FROM
        artist_credit ac
        LEFT OUTER JOIN
        artist_credit_name acn
        ON
        ac.id = acn.artist_credit
    WHERE
        ac.artist_count > 1 -- Only look at collaborations with 2+ collaborators
),
edges_via_credit AS ( -- Cross-join the nodes table with itself and filter the result to find the edges
    SELECT DISTINCT ON (collaborator1, collaborator2)
        node1.collaborator AS collaborator1,
        node2.collaborator AS collaborator2
    FROM
        nodes AS node1
        CROSS JOIN
        nodes AS node2
    WHERE
        node1.collaboration = node2.collaboration
        AND
        node1.collaborator != node2.collaborator
        AND
        node1.collaborator < node2.collaborator -- Avoid duplicate edges
)

INSERT INTO edges (collaborator1, collaborator2)
    SELECT collaborator1, collaborator2 FROM edges_via_credit;
