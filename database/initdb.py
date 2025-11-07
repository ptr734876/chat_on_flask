import os
import sqlite3

def initDB(table_name, columns, db_name):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, db_name)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    columns_sql = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns.items()])

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {columns_sql}
    )
    """)

    conn.commit()
    conn.close()
    return db_path