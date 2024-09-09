import streamlit as st
import pandas as pd
import duckdb

query=st.text_area("Enter your query here")

data={"a":[1,2,3],"b":(4,5,6)}
df=pd.DataFrame(data)

st.dataframe(duckdb.sql(query).df())