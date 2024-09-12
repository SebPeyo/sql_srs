# pylint: disable=(missing-module-docstring)

import duckdb
import streamlit as st

# ------------------------------------------------------------
# Connect to the database
# ------------------------------------------------------------

con = duckdb.connect(database="data/exercises_sql_table.duckdb", read_only=False)

st.write(
    """
# SQL SRS
Spaced Repetition System SQL Practice
"""
)

# ------------------------------------------------------------
# Topic Selection
# ------------------------------------------------------------

with st.sidebar:
    topic = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "CTEs", "Window Functions"),
        index=None,
        placeholder="Select a theme ...",
    )
    if topic:
        st.write(f"You have selected: {topic}")

        exercise = con.execute(
            query="SELECT * FROM memory_state WHERE theme = ?", parameters=(topic,)
        ).df().sort_values(by="last_reviewed").reset_index(drop=True)
        st.dataframe(exercise)

        exercise_name = exercise.loc[0, "exercise_name"]
        with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
            answer = f.read()

        df_answer = con.execute(answer).df()

# ------------------------------------------------------------
# Query input section
# ------------------------------------------------------------

query = st.text_area(label="Enter your SQL code Here")

if query:
    if topic:

        df_query = con.execute(query).df()

        column_diff = df_query.shape[1] - df_answer.shape[1]
        row_diff = df_query.shape[0] - df_answer.shape[0]

        st.dataframe(df_query)

        if row_diff != 0:
            st.write(f"There is a {row_diff} rows difference with the solution!")

        try:
            df_query = df_query[df_answer.columns]

            df_compare = df_query.compare(
                df_answer, result_names=("answer", "solution")
            )

            if df_compare.shape != (0, 0):
                st.dataframe(df_compare)

        except KeyError as e:
            st.write(f"There is a {column_diff} columns difference with the solution!")

    else:
        st.write("Select a topic first ! 😉")

# ------------------------------------------------------------
# Tables and Answer section
# ------------------------------------------------------------

tab1, tab2 = st.tabs(["Tables", "Answer"])

with tab1:
    if topic:
        exercise_tables = exercise.loc[0, "tables"]

        for table in exercise_tables:
            st.write(f"<u>Table</u>: **{table}**", unsafe_allow_html=True)
            df = con.execute(query=f"SELECT * FROM {table}").df()
            st.dataframe(df)

with tab2:
    if topic:
        st.code(answer)
