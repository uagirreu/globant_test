# queries.py

from sqlalchemy import text

GET_EMPLOYEES_BY_QUARTER = text("""
SELECT 
    d.department AS department, 
    j.job AS job,
    SUM(CASE WHEN MONTH(e.datetime) = 1 OR MONTH(e.datetime) = 2 OR MONTH(e.datetime) = 3 THEN 1 ELSE 0 END) AS Q1,
    SUM(CASE WHEN MONTH(e.datetime) = 4 OR MONTH(e.datetime) = 5 OR MONTH(e.datetime) = 6 THEN 1 ELSE 0 END) AS Q2,
    SUM(CASE WHEN MONTH(e.datetime) = 7 OR MONTH(e.datetime) = 8 OR MONTH(e.datetime) = 9 THEN 1 ELSE 0 END) AS Q3,
    SUM(CASE WHEN MONTH(e.datetime) = 10 OR MONTH(e.datetime) = 11 OR MONTH(e.datetime) = 12 THEN 1 ELSE 0 END) AS Q4
FROM 
    employees e
JOIN 
    departments d ON e.department_id = d.id
JOIN 
    jobs j ON e.job_id = j.id
WHERE 
    YEAR(e.datetime) = 2021
GROUP BY 
    d.department, j.job
ORDER BY 
    d.department, j.job;
""")

GET_DEPARTMENTS_ABOVE_AVERAGE = text("""
WITH DepartmentHires AS (
    SELECT 
        d.id AS id,
        d.department AS department,
        COUNT(e.id) AS hired
    FROM 
        employees e
    JOIN 
        departments d ON e.department_id = d.id
    WHERE 
        YEAR(e.datetime) = 2021
    GROUP BY 
        d.id, d.department
),
AverageHires AS (
    SELECT 
        AVG(hired) AS avg_hired
    FROM 
        DepartmentHires
)

SELECT 
    dh.id,
    dh.department,
    dh.hired
FROM 
    DepartmentHires dh
JOIN 
    AverageHires ah ON dh.hired > ah.avg_hired
ORDER BY 
    dh.hired DESC;
""")
