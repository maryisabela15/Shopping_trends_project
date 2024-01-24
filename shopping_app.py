import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


# Create the engine object
engine = create_engine("postgresql+psycopg2://postgres:Perrona123@localhost:5432/postgres")
#engine = create_engine("postgresql+psycopg2://postgres:password@host:port/database")

# Read the data from the postgres table
data = pd.read_sql_table("update_shopping_data", engine)

st.title('Shopping Dataset')

st.divider()

st.subheader('Dataframe example')
st.write(data.head(3))

st.divider()

#########################################################################################
### Create a function

def setup_container(key_column):
   with st.container():
        col1, col2 = st.columns([3,3])
        with col1:
           query = '''
            SELECT DISTINCT region,
                    category,
                    COUNT(*) as total_item
            FROM update_shopping_data
            GROUP BY 1,2
            ORDER BY 1, 3 DESC;
        '''
           result = pd.read_sql_query(query, engine).pivot_table(values='total_item', index='category', columns='region')
           st.write(result)


        with col2:
         fig, ax = plt.subplots(figsize = (8,3))

         ax.pie(result[key_column], labels=result.index, wedgeprops={'width':0.35}, autopct='%1.1f%%', 
              colors=sns.color_palette("Blues"), explode=[0.01, 0.01, 0.01, 0.01], 
              textprops={'fontsize': 14})
         st.pyplot(fig)

         

#### Create a side bar
with st.sidebar:
   selected_location = st.selectbox(
      "Choose a region",
      ("East Coast", "Central", "West Coast", "Outside")
   )
   st.caption(
      """Each region includes all the information about the states that compose it."""
   )
   

st.subheader(f"Total items purchased by category in the {selected_location} region")
setup_container(selected_location)

st.divider()

###################################################################################################
### Second part
st.subheader("Total items purchased and amount in usd by region")

with st.container():
   #, col2 = st.columns([1,2])
   #with col1:
      query1 = '''
         SELECT DISTINCT region,
               COUNT(item_purchased) as total_item_purchased,
               SUM(purchase_amount_usd) as total_amount_usd
         FROM update_shopping_data
         GROUP BY 1
         ORDER BY 2 DESC, 3 DESC;
         '''
      result1 = pd.read_sql_query(query1, engine)
      st.write(result1)


   #with col2:
      fig, ax = plt.subplots(1, 2, sharex= False, figsize=(10,4))

      ax[0].bar(result1['region'], result1['total_item_purchased'], color = sns.color_palette("Blues"))
      ax[0].spines[['right', 'top']].set_visible(False)
      ax[0].set_xlabel('Region')
      ax[0].set_ylabel('Total item')
      ax[0].set_title('a) Total items purchased by region')

      ax[1].bar(result1['region'], result1['total_amount_usd'], color = sns.color_palette("Greens"))
      ax[1].spines[['right', 'top']].set_visible(False)
      ax[1].set_xlabel('Region')
      ax[1].set_ylabel('Total amount')
      ax[1].set_title('b) Total amount in usd by region')
      st.pyplot(fig)

st.divider()   

##############################################################################
### Part 3: Total items purchased per season in each region
st.subheader(f"Total items purchased per season in the {selected_location} region")

def plot_barchart(regions): 
   with st.container():
      col1, col2 = st.columns([4,3])
      with col1:
         query = '''
            SELECT DISTINCT region,
                  season,
                  COUNT(*) as total_item
            FROM update_shopping_data
            GROUP BY 1,2
            ORDER BY 1, 3 DESC;
         '''
         result = pd.read_sql_query(query, engine).pivot_table(values = 'total_item', index = 'season', columns = 'region')
         st.write(result)

      with col2: 
         fig, ax = plt.subplots(figsize = (8,3))
  
         ax.pie(result[regions], labels=result.index, wedgeprops={'width':0.35}, autopct='%1.1f%%', 
              colors=sns.color_palette("Blues"), explode=[0.01, 0.01, 0.01, 0.01], 
              textprops={'fontsize': 14})
         st.pyplot(fig)

plot_barchart(selected_location)      

st.divider()
##################################################################################################
### Part 4: Most used payment method by region    
st.subheader(f"Most used payment method in the {selected_location} region ")

def plot_chart(regions):
   with st.container():
      col1, col2 = st.columns([3,3])
      with col1:
         query = '''
            SELECT DISTINCT region,
               payment_method,
               COUNT(*) as total_payment_method
            FROM update_shopping_data
            GROUP BY 1,2
            ORDER BY 1, 3 DESC;
         '''
         result = pd.read_sql_query(query, engine).pivot_table(values='total_payment_method', index='payment_method', columns='region')
         st.write(result) 

      with col2:
         fig, ax = plt.subplots(figsize = (8,3))

         ax.pie(result[regions], wedgeprops={'width':0.35}, labels=result.index, autopct='%1.1f%%', 
            explode=(0.05, 0.05, 0.05, 0.05, 0.05, 0.05), 
            colors=sns.color_palette("Blues"), textprops={'fontsize':12})
         st.pyplot(fig)

plot_chart(selected_location)    

st.divider()
############################################################################################
### Part 5: Most shipping method used by region
st.subheader(f"Most shipping method used in the {selected_location} region ")

def plot_chart1(regions):
   with st.container():
      col1, col2 = st.columns([3,4])
      with col1: 
         query = '''
            SELECT DISTINCT region,
               shipping_type,
               COUNT(*) as total
            FROM update_shopping_data
            GROUP BY 1,2
            ORDER BY 1, 3 DESC;
         '''
         result = pd.read_sql_query(query, engine).pivot_table(values='total', index='shipping_type', columns='region')
         st.write(result)
   
      with col2:
         fig, ax = plt.subplots(figsize=(12, 5))

         ax.pie(result[regions], wedgeprops={'width':0.35}, labels=result.index, autopct='%1.1f%%', 
            explode=(0.05, 0.05, 0.05, 0.05, 0.05, 0.05), 
            colors=sns.color_palette("Blues"), textprops={'fontsize':20})
         st.pyplot(fig)

plot_chart1(selected_location)