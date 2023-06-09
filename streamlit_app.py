import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents\'s new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit for information")
    else:
      fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
      # Add response to pandas dataframe
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # display dataframe
      streamlit.dataframe(fruityvice_normalized)
except URLERROR as e:
  streamlit.error()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()

streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)


add_my_fruit = streamlit.text_input('Which fruit would you like to add?')
if streamlit.button('Add fruit to list'):
        my_cur.execute(f"insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values(\'{add_my_fruit}\');")
        streamlit.write('Thank you for adding ', add_my_fruit)


