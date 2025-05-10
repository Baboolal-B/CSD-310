import pymysql
from tabulate import tabulate

# Database connection settings (update these)
db_config = {
    "host":"localhost",
    "user":"root",
    "password":"Smokey@1512!",
    "database":"BacchusWinery"
}

# SQL query
query = """
WITH AvgSales AS (
    SELECT 
        AVG(sr.QuantitySold) AS AvgSold
    FROM SalesRecord sr
    JOIN Wine w ON sr.WineID = w.WineID
)
SELECT 
    w.WineType AS WineType,
    w.WineName AS WineName,
    d.Name AS Distributor,
    SUM(sr.QuantitySold) AS TotalBottlesSold
FROM SalesRecord sr
JOIN Wine w ON sr.WineID = w.WineID
JOIN WineDistribution wd ON w.WineID = wd.WineID
JOIN Distributor d ON wd.DistributorID = d.DistributorID
GROUP BY w.WineType, w.WineName, d.Name
HAVING TotalBottlesSold < (SELECT AvgSold FROM AvgSales)
ORDER BY TotalBottlesSold ASC;
"""

connection = None  # Initialize connection variable

try:
    # Connect to the database
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()

    # Get column names
    columns = [desc[0] for desc in cursor.description]

    # Print the results as a table
    print(tabulate(results, headers=columns, tablefmt="grid"))

except pymysql.MySQLError as e:
    print("Error connecting to MySQL:", e)

finally:
    # Close the connection if it's established
    if connection:
        connection.close()
