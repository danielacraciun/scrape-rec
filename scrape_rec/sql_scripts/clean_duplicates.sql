-- keeps newest entries
DELETE
FROM
    realestate a
        USING realestate b
WHERE
    a.posted_date < b.posted_date
    AND a.title = b.title;