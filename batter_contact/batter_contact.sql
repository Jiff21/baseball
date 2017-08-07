SELECT
    *
FROM
    batter_contact_type
WHERE
     `LD%`>=20 AND `Med%`>=42 AND `Hard%`>=40
ORDER BY
    `Hard%` DESC
