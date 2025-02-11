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

# Directory containing all exported CSV files
csv_dir = "./csv_exports"


def table_exists(table_name):
    cursor.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = %s
        );
    """,
        (table_name,),
    )
    return cursor.fetchone()[0]


def table_is_empty(table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    return count == 0


try:
    # Loop through each CSV file in the directory
    for csv_file in os.listdir(csv_dir):
        original_table_name = os.path.splitext(csv_file)[
            0
        ]  # Extract table name from file name

        # Convert CamelCase to snake_case (e.g., DiagnosticFragment to diagnostic_fragment)
        table_name = "".join(
            ["_" + c.lower() if c.isupper() else c for c in original_table_name]
        ).lstrip("_")

        # Prepend 'db_' to the table name (assuming 'db' is your app name)
        django_table_name = f"db_{table_name}"

        csv_file_path = os.path.join(csv_dir, csv_file)

        print(f"Checking {django_table_name}...")

        if not table_exists(django_table_name):
            print(f"Table {django_table_name} does not exist. Skipping...")
            continue

        if table_is_empty(django_table_name):
            print(f"Restoring {django_table_name} from {csv_file_path}...")
            with open(csv_file_path, "r", encoding="utf-8") as f:
                cursor.copy_expert(
                    f'COPY "{django_table_name}" FROM STDIN WITH CSV HEADER', f
                )
            print(f"Successfully restored {django_table_name}")
        else:
            print(f"Skipping {django_table_name} as it already contains data")

    # Commit all changes
    conn.commit()
except Exception as e:
    print("An error occurred while restoring tables:", e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()
