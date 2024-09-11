# pylint: disable=(missing-module-docstring)

import io

import duckdb
import pandas as pd

con = duckdb.connect(database="data/exercises_sql_table.duckdb", read_only=False)

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------

data = {
    "theme": ["Joins", "GroupBy"],
    "exercise_name": ["beverages_and_food", "simple_groupby"],
    "tables": [["beverages", "food_items"], "simple_groupby"],
    "last_reviewed": ["2024-09-11", "2024-09-11"],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE OR REPLACE TABLE memory_state AS SELECT * FROM memory_state_df")

# ------------------------------------------------------------
# CROSS JOIN
# ------------------------------------------------------------
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE OR REPLACE TABLE beverages AS SELECT * FROM beverages")


CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE OR REPLACE TABLE food_items AS SELECT * FROM food_items")
