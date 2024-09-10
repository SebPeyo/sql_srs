import streamlit as st
import pandas as pd
import duckdb

st.write("""
# SQL SRS
Spaced Repetition System SQL Practice
""")

theme = st.selectbox(label="What would you like to review ?"
             ,options = ["Joins","GroupBy","Window Functions","CTEs"]
             ,index = None
             ,placeholder= "Select a theme ...")

st.write(f"You have selected: {theme}")

query=st.text_area("Enter your query here")
st.write(f"You have entered the following query: {query}")

data={"a":[1,2,3],"b":(4,5,6)}
df=pd.DataFrame(data)

st.dataframe(duckdb.sql(query).df())