"""
One-off fix for out-of-sync PostgreSQL sequences after a data reload.

Run it through Django's shell so it uses your existing DB connection (psycopg),
no `psql` client required:

    python manage.py shell < fix_sequences.py

It walks every table in the `public` schema, finds the sequence behind its
primary key (works for both serial and identity columns), and sets it to the
current MAX(id) so the next insert gets a fresh, non-colliding id. Tables with
no sequence (e.g. Glycan's LBG-xxxxx char PK) are skipped automatically.
"""

from django.db import connection

SQL = """
DO $$
DECLARE r RECORD;
BEGIN
    FOR r IN
        SELECT n.nspname || '.' || c.relname AS tbl,
               a.attname AS col,
               pg_get_serial_sequence(n.nspname || '.' || c.relname, a.attname) AS seq
        FROM pg_class c
        JOIN pg_attribute a ON a.attrelid = c.oid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relkind = 'r'
          AND n.nspname = 'public'
          AND pg_get_serial_sequence(n.nspname || '.' || c.relname, a.attname) IS NOT NULL
    LOOP
        EXECUTE format(
            'SELECT setval(%L, COALESCE((SELECT MAX(%I) FROM %s), 1), '
            '(SELECT MAX(%I) FROM %s) IS NOT NULL)',
            r.seq, r.col, r.tbl, r.col, r.tbl
        );
    END LOOP;
END $$;
"""

with connection.cursor() as cur:
    cur.execute(SQL)

print("All sequences resynced.")
