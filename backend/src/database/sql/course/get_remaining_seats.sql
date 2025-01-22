SELECT
    [sn],
    [座位號]
FROM
    [JLL2].[dbo].[學生補位明細]
WHERE
    主檔號 = 4
    AND 學號 IS NULL