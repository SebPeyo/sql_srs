# pylint: disable=(missing-module-docstring)

import io

import duckdb
import pandas as pd
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_table.duckdb", read_only=False)

# APP CODE

st.write(
    """
# SQL SRS
Spaced Repetition System SQL Practice
"""
)

with st.sidebar:
    topic = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "CTEs", "Window Functions"),
        index=None,
        placeholder="Select a theme ...",
    )

    st.write(f"You have selected: {topic}")
    exercise=con.execute("SELECT * FROM memory_state WHERE theme = ?",parameters=(topic,)).df()
    st.dataframe(exercise)

query = st.text_area(label="Enter your SQL code Here")

# if query:
#     df_query = duckdb.sql(query).df()
#
#     column_diff = df_query.shape[1] - df_answer.shape[1]
#     row_diff = df_query.shape[0] - df_answer.shape[0]
#
#     if row_diff != 0:
#         st.write(f"There is a {row_diff} rows difference with the solution!")
#
#     try:
#         df_query = df_query[df_answer.columns]
#
#         df_compare = df_query.compare(df_answer, result_names=("answer", "solution"))
#
#         if df_compare.shape != (0, 0):
#             st.dataframe(df_compare)
#
#     except KeyError as e:
#         st.write(f"There is a {column_diff} columns difference with the solution!")
#
#     st.dataframe(df_query)
#
# tab1, tab2 = st.tabs(["Tables", "Answer"])
#
# with tab1:
#     st.write("Expected")
#     st.dataframe(df_answer)
#
#     st.write("Table: beverages")
#     st.dataframe(beverages)
#
#     st.write("Table: food_items")
#     st.dataframe(food_items)
#
# with tab2:
#     st.write(QUERY_STR)
