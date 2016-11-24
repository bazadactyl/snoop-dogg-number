-- TODO: Add description.

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
    SELECT
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
INSERT INTO weighted_edges (collaborator1, collaborator2, num_collabs)
    SELECT collaborator1, collaborator2, COUNT(*) AS num_collabs
    FROM edges_via_credit
    GROUP BY collaborator1, collaborator2
    ORDER BY collaborator1, collaborator2;
