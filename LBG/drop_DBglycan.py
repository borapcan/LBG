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

try:
    # Use TRUNCATE to delete all rows (faster and resets sequences for IDs)
    cursor.execute('TRUNCATE TABLE "DB_glycan" RESTART IDENTITY CASCADE;')

    # Or use DELETE (slower, doesn't reset sequences)
    # cursor.execute('DELETE FROM "DB_glycan";')

    conn.commit()
    print("All rows from DB_glycan have been deleted.")
except Exception as e:
    print("An error occurred:", e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()
