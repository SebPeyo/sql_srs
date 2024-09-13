# pylint: disable=(missing-module-docstring)

import duckdb
import pandas as pd

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------

data = {
    "theme": ["Joins", "Joins", "Joins"],
    "exercise_name": [
        "beverages_and_food",
        "sizes_and_trademarks",
        "hours_and_quarters",
    ],
    "tables": [
        ["beverages", "food_items"],
        ["sizes", "trademarks"],
        ["hours", "quarters"],
    ],
    "last_reviewed": [
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
    ],
    "question": [
        "Do a CROSS JOIN with the two tables.",
        "Do a CROSS JOIN with the two tables.",
        "Join the two tables to obtain every quarter from 8:00 to 12:45",
    ],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE OR REPLACE TABLE memory_state AS SELECT * FROM memory_state_df")

# ------------------------------------------------------------
# Creation of the tables
# ------------------------------------------------------------
tables = pd.read_csv("data/tables.csv")

for row in tables.iterrows():
    table_name = row[1]["name"]
    link = row[1]["link"]
    df = pd.read_csv(link)
    query = f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df"
    con.execute(query)

con.close()
