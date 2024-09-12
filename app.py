# pylint: disable=(missing-module-docstring)
import logging
import os

import duckdb
import pandas as pd
import streamlit as st

# ------------------------------------------------------------
# Initialize the db on streamlit if not found
# ------------------------------------------------------------

if "data" not in os.listdir():
    logging.debug(os.listdir())
    logging.debug("Creating data folder ...")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())  # pylint: disable=all

# ------------------------------------------------------------
# Connect to the database
# ------------------------------------------------------------

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

st.write(
    """
# SQL SRS
##### Spaced Repetition System SQL Practice
"""
)

# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------

def check_user_solution(user_query: str) -> None:
    """
    Check whether the user's SQL query is correct by:
    1. Checking the number of rows/columns
    2. Checking the values
    :param user_query: a string containing the query inserted by the user
    """
    df_query = con.execute(user_query).df()
    column_diff = df_query.shape[1] - df_answer.shape[1]
    row_diff = df_query.shape[0] - df_answer.shape[0]
    st.dataframe(df_query)
    if row_diff != 0:
        st.write(f"There is a {row_diff} rows difference with the solution!")
    try:
        df_query = df_query[df_answer.columns]

        df_compare = df_query.compare(df_answer, result_names=("answer", "solution"))

        if df_compare.shape != (0, 0):
            st.dataframe(df_compare)

    except KeyError:
        st.write(f"There is a {column_diff} columns difference with the solution!")

def get_topic() -> str:
    """
    Define the SQL topic to train on based on the user input.
    :return: the name of the topic
    """
    global topic
    available_themes = (
        con.execute("SELECT DISTINCT theme FROM memory_state").df().values
    )
    topic = st.selectbox(
        "What would you like to review?",
        available_themes,
        index=None,
        placeholder="Select a theme ...",
    )
    return topic

def get_exercise(user_topic: str) -> pd.DataFrame:
    """
    Returns a DataFrame with all the available exercises based on the user topic selection.
    :param user_topic: The topic selected by the user (default None if no topic selected)
    :return: DataFrame containing the exercises
    """
    global exercise
    if user_topic:
        topic_query = f"SELECT * FROM memory_state WHERE theme ='{user_topic}'"
        st.write(f"You have selected: **{user_topic}**")
    else:
        topic_query = "SELECT * FROM memory_state"
    exercise = (
        con.execute(query=topic_query)
        .df()
        .sort_values(by="last_reviewed")
        .reset_index(drop=True)
    )
    return exercise
# ------------------------------------------------------------
# Topic and Exercise Selection
# ------------------------------------------------------------

def get_solution(exercises: pd.DataFrame) -> str:
    """
    Returns the answer of the least recently reviewed exercises
    :param exercises: DataFrame containing all the exercises for a pre-selected topic
    :return: A SQL query that solves the exercise
    """
    global answer
    exercise_name = exercises.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
        answer = f.read()
    return answer


with st.sidebar:
    topic=get_topic()
    exercise=get_exercise(topic)
    answer=get_solution(exercise)
    df_answer = con.execute(answer).df()
# ------------------------------------------------------------
# Query input section
# ------------------------------------------------------------

query = st.text_area(label="Enter your SQL code Here")

if query:
    check_user_solution(query)

# ------------------------------------------------------------
# Tables and Answer section
# ------------------------------------------------------------

tab1, tab2 = st.tabs(["Tables", "Answer"])

with tab1:

    exercise_tables = exercise.loc[0, "tables"]

    for table in exercise_tables:
        st.write(f"<u>Table</u>: **{table}**", unsafe_allow_html=True)
        df = con.execute(query=f"SELECT * FROM {table}").df()
        st.dataframe(df)

with tab2:
    st.code(answer)
