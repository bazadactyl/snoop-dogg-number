-- This SQL query populates the nodes table with all the artists who exist in
-- the edges table. This means that artists who haven't collaborated with anyone
-- won't appear here.

WITH
nodes_tmp AS ( -- Each row of this table has a "collaboration" and one of its "collaborators"
    SELECT collaborator1 AS artist FROM unweighted_edges
    UNION ALL
    SELECT collaborator2 AS artist FROM unweighted_edges
)
INSERT INTO nodes (artist)
    SELECT DISTINCT artist
    FROM nodes_tmp
    ORDER BY artist;
