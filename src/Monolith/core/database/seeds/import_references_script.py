import sqlite3
import csv
from pathlib import Path

def import_references():

    files_mapping = {
        'countries.csv': 'countries',
        'doccat.csv': 'document_categories',
        'filetypes.csv': 'file_types',
        'sectors.csv': 'sectors',
        'sourcetype.csv': 'source_types'
    }

    DB_PATH = Path("src/Monolith/core/database/references.db")
    DATA_DIR = Path("src/Monolith/core/database/seeds/")

    # Connection to database
    db_filename = DB_PATH.resolve()
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    for file_name, table_name in files_mapping.items():
        file_path = DATA_DIR / file_name
        
        with open(file_path, mode='r', encoding='utf-8', errors='ignore') as f:
            
            # skipinitialspace=True ensures fields like ', "text"' parse correctly
            reader = csv.reader(f, skipinitialspace=True)
            
            # Extract headers and clean them up for SQL compatibility
            headers = next(reader)
            cleaned_headers = [col.strip().replace(' ', '_').lower() for col in headers]
            
            # Dynamically build the table schema definition (all text fields initially)
            columns_def = ", ".join([f"{col} TEXT" for col in cleaned_headers])
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            cursor.execute(f"CREATE TABLE {table_name} ({columns_def});")
            
            # Prepare the multi-row insert query
            placeholders = ", ".join(["?"] * len(cleaned_headers))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            
            # Gather all rows and insert them en masse
            rows = [row for row in reader if row]
            cursor.executemany(insert_query, rows)
            
        print(f" -> Table '{table_name}' created with {len(rows)} rows from '{file_name}'.")

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print(f"\nAll 5 tables have been successfully saved into '{db_filename}'!")

if __name__ == "__main__":
    import_references()