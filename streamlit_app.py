
# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# DB connection
# Running on Snowflake Streamlit
# session = get_active_session()

# Running on Streamlit
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie."""
)

my_dataframe = session.table("fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect("Chooose up to 5 ingredients:",
                     my_dataframe)

if ingredients_list:
    # Structure
    # st.write(ingredients_list)
    # Text
    # st.text(ingredients_list)
    
    # st.write(f"You selected: {option}")
    ingredients_str = ''
    for fc in ingredients_list:
        ingredients_str += f'{fc} '
    # st.text(ingredients_str)

    insert_stm = f"""INSERT INTO orders(ingredients)
                VALUES ('{ingredients_str}')"""
    # st.write(insert_stm)
    if insert := st.button('Submit Order'):
        r = session.sql(insert_stm).collect()
        # st.write(r)
        st.success('You Smoothe is ordered!', icon="✅")
    
    
        
