import mysql.connector

# Connects to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Smokey@1512!",
    database="BacchusWinery"
)
cursor = conn.cursor()

tables = [
    "Supplier", "SupplyDelivery", "InventoryItem", "ProductionBatch",
    "Wine", "Distributor", "WineDistribution", "Employee", "TimeLog", "SalesRecord"
]

for table in tables:
    print(f"\n--- {table} ---")
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

cursor.close()
conn.close()
