# Import python packages
import streamlit as st
import requests
import pandas as pd
import json
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

from snowflake.snowpark.functions import col

#session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# Convert Snowpark Dataframe to Pandas Dataframe
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

name_on_order = st.text_input("Name on Smoothie:")
#st.write("The name on your Smoothie will be:", name_on_order)
st.info("The name on your Smoothie will be: " + name_on_order)
if name_on_order:
    st.balloons()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)

if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen +' nutrition information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        json_data=fruityvice_response.json()
        try:
            json_tab=json_data['nutritions']
        except:
            json_tab=json.loads('{"No data": ""}')
            
        fv_df=st.dataframe(
            #data=fruityvice_response.json(),
            data=json_tab,
            hide_index=False,
            use_container_width=True)

        #st.dataframe(fv_df.style.highlight_max(axis=0))
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    #st.write(my_insert_stmt)

    time_to_insert = st.button("Submit order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")



