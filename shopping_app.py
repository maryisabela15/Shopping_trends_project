import pandas as pd
import streamlit as st
import psycopg2
from matplotlib import pyplot as plt
import seaborn as sns

# Initialize connection
my_cnx = psycopg2.connect(**st.secrets["postgresql"])
my_cur = my_cnx.cursor()

my_cur.execute('''SELECT DISTINCT region,
                     shipping_type,
                     COUNT(*) as total
                  FROM update_shopping_data
                  GROUP BY 1,2
                  ORDER BY 1, 3 DESC;
               ''')
result = my_cur.fetchall()
st.dataframe(result)

