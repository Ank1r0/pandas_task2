from database.connection import DatabaseManager
import pandas as pd
import os
import csv
from datetime import datetime


def import_csv_to_postgres():
    # 1. Handle the file path dynamically
    # This points to: ..\special_task\data\task_2_data_ex.csv relative to your main.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(
        current_dir, "..", "special_task", "data", "task_2_data_ex.csv"
    )

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    # 2. Read the data
    print("Reading CSV...")
    df = pd.read_csv(file_path)

    # 3. Connect and Upload
    db = DatabaseManager()
    engine = db.get_engine()

    print("Uploading to Postgres...")
    # 'if_exists=replace' creates the table automatically based on your columns
    df.to_sql("material_production", engine, if_exists="replace", index=False)
    print("Success! Data imported into table 'material_production'.")


def main():
    print("App started.")
    # Usage:
    db = DatabaseManager()
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            print(cur.fetchone())

            import_csv_to_postgres()

            sqlfile = open("sqlQuery.sql", "r")
            cur.execute(sqlfile.read())

            someinfo = cur.fetchall()

            headers = [desc[0] for desc in cur.description]

            with open(
                f"SQL_final_result_{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.csv",
                "w",
                newline="",
                encoding="utf-8",
            ) as f:
                writer = csv.writer(f)

                # Write the header first
                writer.writerow(headers)

                # Write all the data rows
                writer.writerows(someinfo)

            print(f"Done! Created output.csv with {len(someinfo)} rows.")


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
