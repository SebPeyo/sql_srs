# pylint: disable=(missing-module-docstring)

import io

import duckdb
import pandas as pd
import streamlit as st

# DATA

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

# ANSWER

QUERY_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

df_answer = duckdb.sql(QUERY_STR).df()

# APP CODE

st.write(
    """
# SQL SRS
Spaced Repetition System SQL Practice
"""
)

query = st.text_area(label="Enter your SQL code Here")

if query:
    df_query = duckdb.sql(query).df()

    column_diff = df_query.shape[1] - df_answer.shape[1]
    row_diff = df_query.shape[0] - df_answer.shape[0]

    if row_diff != 0:
        st.write(f"There is a {row_diff} rows difference with the solution!")

    try:
        df_query = df_query[df_answer.columns]

        df_compare = df_query.compare(df_answer, result_names=("answer", "solution"))

        if df_compare.shape != (0, 0):
            st.dataframe(df_compare)

    except KeyError as e:
        st.write(f"There is a {column_diff} columns difference with the solution!")

    st.dataframe(df_query)

tab1, tab2 = st.tabs(["Tables", "Answer"])

with tab1:
    st.write("Expected")
    st.dataframe(df_answer)

    st.write("Table: beverages")
    st.dataframe(beverages)

    st.write("Table: food_items")
    st.dataframe(food_items)

with tab2:
    st.write(QUERY_STR)
