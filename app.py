import streamlit as st
import pandas as pd
import duckdb
import io

# DATA

csv = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(csv))

csv2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(csv2))

# ANSWER

query_answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

df_answer = duckdb.sql(query_answer).df()

# APP CODE

st.write(
    """
# SQL SRS
Spaced Repetition System SQL Practice
"""
)

with st.sidebar:
    theme = st.selectbox(
        label="What would you like to review ?",
        options=["Joins", "GroupBy", "Window Functions", "CTEs"],
        index=None,
        placeholder="Select a theme ...",
    )

    st.write(f"You have selected: {theme}")

query = st.text_area(label="Enter your SQL code Here")

if query:
    st.dataframe(duckdb.sql(query))

tab1, tab2 = st.tabs(["Tables", "Answer"])

with tab1:
    st.write("Expected")
    st.dataframe(df_answer)

    st.write("Table: beverages")
    st.dataframe(beverages)

    st.write("Table: food_items")
    st.dataframe(food_items)

with tab2:
    st.write(query_answer)
