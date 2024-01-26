import streamlit as st
import psycopg2
import pandas as pd

# Initialize connection
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgresql"])

conn = init_connection()

# Perform query
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
result = run_query("SELECT * FROM update_shopping_data LIMIT 5;")
data = pd.DataFrame(result)
st.write(data)