
# Import python packages
import streamlit as st
import pandas as pd
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# DB connection
# Running on Snowflake Streamlit
# session = get_active_session()

# Running on Streamlit
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
name_on_order = st.text_input('Name on Smoothie:')
st.write(f'The name on your Smoothie will be: {name_on_order}')
st.write(
    """Choose the fruits you want in your custom Smoothie."""
)

my_dataframe = session.table("fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# pandas dataframe
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect("Chooose up to 5 ingredients:",
                     my_dataframe,
                     max_selections=5)

if ingredients_list:
    # Structure
    # st.write(ingredients_list)
    # Text
    # st.text(ingredients_list)
    
    # st.write(f"You selected: {option}")
    ingredients_str = ''
    for fc in ingredients_list:
        ingredients_str += f'{fc} '
        # get the right fruit to search on - using pandas selector / projection
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fc, 'SEARCH_ON'].iloc[0]
        st.write(f'The search value for {fc} is {search_on}')
        # Display nutrition info
        # fruityvice_resp = requests.get(f"https://fruitvice.com/api/fruit/{search_on}")
        # fruit_data = fruityvice_resp.json()
        fruit_data = {
            "name": fc,
            "id": 12345,
            "family": "Something",
            "order": "Somethinis",
            "genus": "Somethinus",
            "nutritions": {
                "calories": 123,
                "fat": 0.2,
                "sugar": 200,
                "carbohydrates": 30,
                "protein": 0.5,
            }
        }
        st.header(f"{fc} Nutrition data")
        fv_df = st.dataframe(data=fruit_data, use_container_width=True)
    # st.text(ingredients_str)

    insert_stm = f"""INSERT INTO orders(ingredients, name_on_order)
                VALUES ('{ingredients_str}', '{name_on_order}')"""
    # st.write(insert_stm)
    if insert := st.button('Submit Order'):
        r = session.sql(insert_stm).collect()
        # st.write(r)
        st.success(f'You Smoothe is ordered, {name_on_order}!', icon="✅")
    
    
        
