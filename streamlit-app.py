from urllib.error import URLError

import pandas as pd
import requests as req
import snowflake.connector as sf_conn
import streamlit as st

st.title("My Parents New Healthy Diner")

st.header("Breakfast Menu")
st.text("🥣 Omega 3 & Blueberry Oatmeal")
st.text("🥗 Kale, Spinach & Rocket Smoothie")
st.text("🐔 Hard-Boiled Free-Range Egg")
st.text("🥑🍞 Avocado Toast")

st.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")
fruit_df = pd.read_csv(
    filepath_or_buffer="https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
)
fruit_df = fruit_df.set_index(keys="Fruit")

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = st.multiselect(
    label="Pick some fruits:",
    options=list(fruit_df.index),
    default=["Banana", "Strawberries"],
)
fruits_to_show = fruit_df.loc[fruits_selected]

if len(fruits_to_show) > 0:
    # Display the table on the page
    st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")
fruityvice_response = req.get("https://fruityvice.com/api/fruit/all")
fruityvice_df = pd.json_normalize(fruityvice_response.json())

fruityvice_df = fruityvice_df.set_index(keys="name")

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected_fv = st.multiselect(
    label="What fruit would you like information about?",
    options=list(fruityvice_df.index),
    default=["Banana"],
)
fruits_to_show_fv = fruityvice_df.loc[fruits_selected_fv]

if len(fruits_to_show_fv) > 0:
    # Display the table on the page
    st.dataframe(fruits_to_show_fv)
else:
    # Display error message
    st.error("Please select a fruit to get information.")

st.header("View Our Fruit List - Add Your Favorites!")
if st.button("Get Fruit Load List"):
    conn = sf_conn.connect(**st.secrets["snowflake"])
    my_cur = conn.cursor()
    my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
    my_data_row = my_cur.fetchall()
    st.dataframe(my_data_row)
val = st.text_input("What fruit would you like to add?")
but = st.button("Add Fruit to the List")
if val and but:
    conn = sf_conn.connect(**st.secrets["snowflake"])
    my_cur = conn.cursor()
    my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
    my_data_row = my_cur.fetchall()
    fruit_list = [item[0] for item in my_data_row]
    if val not in fruit_list:
        my_cur.execute(
            f"INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('{val}')"
        )
        st.text(f"Thanks for adding {val}")
    else:
        st.text(f"{val.capitalize()} is already on the list")
