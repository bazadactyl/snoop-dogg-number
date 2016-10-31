-- This SQL query populates the table containing  the number of collaborators
-- each artist has collaborated with. This aggregation is performed using the
-- edges table.

INSERT INTO collaborator_count (artist, count) (
    SELECT
        artist,
        count(*) AS count
    FROM (
        SELECT collaborator1 AS artist FROM edges
        UNION ALL
        SELECT collaborator2 AS artist FROM edges
    ) t
    GROUP BY artist
    ORDER BY count DESC
);
