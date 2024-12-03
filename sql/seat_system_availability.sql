SELECT
    TOP 1 [學生補位主檔].*
FROM
    [學生補位主檔]
WHERE
    getdate() BETWEEN [學生補位主檔].開始時間
    AND [學生補位主檔].結束時間