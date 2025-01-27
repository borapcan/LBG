import psycopg2
import os

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="DB",
    user="postgres",
    password="admin",
)
cursor = conn.cursor()


# Fetch all table names from the public schema
cursor.execute(
    """
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public';
"""
)
tables = cursor.fetchall()

# Directory to save the CSV files
output_dir = "./csv_exports"
os.makedirs(output_dir, exist_ok=True)

# Export each table to a CSV file
for table in tables:
    table_name = table[0]
    csv_path = os.path.join(output_dir, f"{table_name}.csv")
    with open(csv_path, "w", encoding="utf-8") as f:  # Set UTF-8 encoding
        cursor.copy_expert(f'COPY "{table_name}" TO STDOUT WITH CSV HEADER', f)
        print(f"Exported {table_name} to {csv_path}")

# Close the connection
conn.close()
