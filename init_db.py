# pylint: disable=(missing-module-docstring)

import io

import duckdb
import pandas as pd

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------

data = {
    "theme": ["Joins", "Joins"],
    "exercise_name": ["beverages_and_food", "sizes_and_trademarks"],
    "tables": [["beverages", "food_items"], ["sizes", "trademarks"]],
    "last_reviewed": ["2024-09-12", "2024-09-11"],
    "question": [
        "Do a CROSS JOIN with the two tables.",
        "Do a CROSS JOIN with the two tables.",
    ],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE OR REPLACE TABLE memory_state AS SELECT * FROM memory_state_df")

# ------------------------------------------------------------
# CROSS JOIN - foods and beverages
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

# ------------------------------------------------------------
# CROSS JOIN - sizes and trademarks
# ------------------------------------------------------------
SIZES = """
size
XS
M
L
XL
"""

sizes = pd.read_csv(io.StringIO(SIZES))
con.execute("CREATE OR REPLACE TABLE sizes AS SELECT * FROM sizes")

TRADEMARKS = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""

trademarks = pd.read_csv(io.StringIO(TRADEMARKS))
con.execute("CREATE OR REPLACE TABLE trademarks AS SELECT * FROM trademarks")

con.close()
