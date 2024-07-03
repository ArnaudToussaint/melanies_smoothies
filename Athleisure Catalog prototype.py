# Import python packages
import streamlit as st
import pandas as pd
import requests
import json
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title("Zena's Amazing Athleisure Catalog")

my_dataframe = session.table("zenas_athleisure_db.products.color_or_style_for_website").select(col("color_or_style"),col("file_name"))
catalog_data = session.table("zenas_athleisure_db.products.catalog_for_website")
pd_df = catalog_data.to_pandas()

color_option = st.selectbox(
    "Pick a sweatsuit color or style:",
    my_dataframe,
    index=None,
    placeholder="Select color...",
)

#st.session_state['df'] = catalog_data
#st.dataframe(my_dataframe)
#df_filtered = df.filter((col("A") > 1) & (col("B") < 100))
#make_choice = st.sidebar.selectbox('Select your vehicle:', makes)

if color_option:
    st.write("You selected:" , color_option)
    item_selected = catalog_data.filter((col("color_or_style") == color_option))
    st.table(item_selected)
    st.dataframe(item_selected)

    df = pd.DataFrame({'Item': ['Bagel', 'Coffee', 'Smart TV'], 'Price (Coins)': [125, 110, 7000]})
    st.table(df)
    selected_reward = st.selectbox("Choose a reward", df.Item, 0)
    selected_reward_price = df.loc[df.Item == selected_reward]["Price (Coins)"].iloc[0]
    st.write(f'Price: {selected_reward_price}')
    
    item_pic = item_selected.columns('FILE_URL')
    st.image(item_pic)
else:
    st.info("No selection")
