import psycopg2
import os

# Database connection details
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="DB",
    user="postgres",
    password="admin",
)
cursor = conn.cursor()

# List of tables and their corresponding CSV file paths
tables_and_files = [
    ("DB_glycan", "./csv_exports/DB_glycan.csv"),
    ("DB_glycan_model_species", "./csv_exports/DB_glycan_model_species.csv"),
    ("DB_glycan_studies", "./csv_exports/DB_glycan_studies.csv"),
]

try:
    for table, csv_file_path in tables_and_files:
        # Open the CSV file for reading
        with open(csv_file_path, "r", encoding="utf-8") as f:
            # Use COPY command to import data into the table
            cursor.copy_expert(f'COPY "{table}" FROM STDIN WITH CSV HEADER', f)

        print(f"Data successfully restored to {table} from {csv_file_path}")

    # Commit changes
    conn.commit()
    print("All data has been successfully imported.")
except Exception as e:
    print("An error occurred while importing data:", e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()
