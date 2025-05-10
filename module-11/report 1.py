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
SELECT
    s.Name AS SupplierName,
    DATE_FORMAT(sd.ExpectedDeliveryDate, '%Y-%m') AS Month,
    AVG(DATEDIFF(sd.DeliveryDate, sd.ExpectedDeliveryDate)) AS AvgDelayDays,
    GROUP_CONCAT(DISTINCT DATE_FORMAT(sd.ExpectedDeliveryDate, '%Y-%m-%d') ORDER BY sd.ExpectedDeliveryDate SEPARATOR ', ') AS ExpectedDates,
    GROUP_CONCAT(DISTINCT DATE_FORMAT(sd.DeliveryDate, '%Y-%m-%d') ORDER BY sd.DeliveryDate SEPARATOR ', ') AS ActualDeliveryDates
FROM SupplyDelivery sd
JOIN Supplier s ON sd.SupplierID = s.SupplierID
GROUP BY s.Name, Month
ORDER BY s.Name, Month;
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
