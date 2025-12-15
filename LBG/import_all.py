import os
import psycopg2

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

# Set schema you use (Django default on Postgres is usually "public")
SCHEMA = "public"


def existing_tables(schema=SCHEMA):
    cursor.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s AND table_type = 'BASE TABLE';
        """,
        (schema,),
    )
    return {row[0] for row in cursor.fetchall()}


def table_is_empty(schema, table_name):
    # Use schema-qualified name; quote identifiers to be safe
    cursor.execute(f'SELECT COUNT(*) FROM "{schema}"."{table_name}"')
    return cursor.fetchone()[0] == 0


def resolve_table_name(csv_stem, tables_set):
    """
    Try to map a CSV filename stem to an actual table name.
    - exact match
    - case-insensitive match
    - CamelCase -> snake_case match
    """
    if csv_stem in tables_set:
        return csv_stem

    lower_map = {t.lower(): t for t in tables_set}
    if csv_stem.lower() in lower_map:
        return lower_map[csv_stem.lower()]

    # CamelCase -> snake_case
    snake = "".join(["_" + c.lower() if c.isupper() else c for c in csv_stem]).lstrip("_")
    if snake in tables_set:
        return snake
    if snake.lower() in lower_map:
        return lower_map[snake.lower()]

    return None


try:
    tables = existing_tables(SCHEMA)

    if not os.path.isdir(csv_dir):
        raise FileNotFoundError(f"CSV directory not found: {os.path.abspath(csv_dir)}")

    for csv_file in sorted(os.listdir(csv_dir)):
        if not csv_file.lower().endswith(".csv"):
            continue

        csv_stem = os.path.splitext(csv_file)[0]
        csv_file_path = os.path.join(csv_dir, csv_file)

        table_name = resolve_table_name(csv_stem, tables)

        print(f"Checking CSV '{csv_file}' -> table '{table_name}'...")

        if not table_name:
            print(f"No matching table found for '{csv_stem}'. Skipping...")
            continue

        if table_is_empty(SCHEMA, table_name):
            print(f"Restoring {SCHEMA}.{table_name} from {csv_file_path}...")
            with open(csv_file_path, "r", encoding="utf-8") as f:
                cursor.copy_expert(
                    f'COPY "{SCHEMA}"."{table_name}" FROM STDIN WITH CSV HEADER',
                    f,
                )
            print(f"Successfully restored {SCHEMA}.{table_name}")
        else:
            print(f"Skipping {SCHEMA}.{table_name} (already contains data)")

    conn.commit()

except Exception as e:
    print("An error occurred while restoring tables:", e)
    conn.rollback()

finally:
    cursor.close()
    conn.close()
