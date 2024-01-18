import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import numpy as np
from matplotlib.pyplot import plot

# Read the csv file
df = pd.read_csv('/home/maria91/Documents/Data_Analyst/SQL/Project_7/shopping_trends_updated.csv')

# Create the engine object
engine = create_engine("postgresql+psycopg2://postgres:Perrona123@localhost:5432/postgres")

# Clean column names
df.columns = df.columns.str.lower()

def clean_col_names(df):
    def clean_col_names(name):
        clean_name = name.replace(' ', '_').replace('(', '').replace(')', '')
        return clean_name
        
    df.columns = [clean_col_names(col) for col in df.columns]
    return df

df = clean_col_names(df)

df.head()


# Save the dataframe into postgres database
#df.to_sql("shopping_data", engine, index = False)

# Read the data from the postgres table
data = pd.read_sql_table("shopping_data", engine)

st.subheader('This is an example of a Dataframe')
st.write(data.head(3))

st.divider()

# Create a container with three tables to put information on it
tab1, tab2, tab3 = st.tabs(["Table 1", "Table 2", "Table 3"])

# Insert elements into each tab
with tab1:
   st.subheader('Total purchased by category')
   query = '''
        SELECT category,
               COUNT(*)
        FROM shopping_data
        GROUP BY 1
        ORDER BY 2 DESC;
    '''
   result = pd.read_sql_query(query, engine)
   st.write(result)


with tab2:
   st.subheader('Item purchased by category')
   query1 = '''
           SELECT category,
                  item_purchased,
                  COUNT(*) as total
            FROM shopping_data
            GROUP BY 1,2
            ORDER BY 1, 3 DESC;
    '''
   result1 = pd.read_sql_query(query1, engine)
   st.write(result1)

with tab3:
   st.subheader('Total purchase amount by category')
   query2 = '''
            SELECT category,
                   item_purchased,
                   SUM(purchase_amount_usd) as total_usd
            FROM shopping_data
            GROUP BY 1,2
            ORDER BY 1, 2;
    '''
   result2 = pd.read_sql_query(query2, engine)
   st.write(result2)

#########################################################################################
   
# Create a container with three tables to put information on it
tab1, tab2, tab3 = st.tabs(["Table 1", "Table 2", "Table 3"])

# Insert elements into each tab
with tab1:
   st.subheader('Total item purchased by season')
   query = '''
        SELECT season,
               COUNT(item_purchased) as total_items
        FROM shopping_data
        GROUP BY 1
        ORDER BY 2 DESC;
    '''
   result = pd.read_sql_query(query, engine)
   st.write(result)


with tab2:
   st.subheader('Total item purchased by location basen on season')
   query1 = '''
            SELECT location,
                   season,
                   COUNT(item_purchased)
            FROM shopping_data
            GROUP BY 1,2
            ORDER BY 1, 2;
    '''
   result1 = pd.read_sql_query(query1, engine)
   st.write(result1)

with tab3:
   st.subheader('Total purchase amount by location and season')
   query3 = '''
            SELECT location,
                   season,
                   SUM(purchase_amount_usd) as total_usd
            FROM shopping_data
            GROUP BY 1,2
            ORDER BY 1, 2;
    '''
   result3 = pd.read_sql_query(query3, engine)
   st.write(result3)   


#########################################################################################
### Create a sidebar ######################
      
with st.sidebar:
    selected_gender = st.selectbox(
        "Choose a gender",
        ("Female", "Male")
    )

with st.sidebar:
    selected_location = st.selectbox(
        "Choose a location",
        ("Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
         "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
         "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Lousiana",
         "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
         "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
         "New Mexico", "New York", "North Carolina", "Norh Dakota", "Ohio",
         "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
         "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", 
         "Washington", "West Virginia", "Wisconsin", "Wyoming")
    )
    
