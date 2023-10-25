import pandas as pd
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
