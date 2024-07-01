import random
import pandas as pd
import streamlit as st
import requests
import json

worldbank_response=requests.get('https://api.worldbank.org/v2/country/FR/indicator/SP.POP.TOTL?date=2011:2020&format=json')
json_results=worldbank_response.json()

#try:
#    json_tab=json_results['nutritions']
#except:
#    json_tab=json.loads('{"No data": ""}')


df0 = st.dataframe(
    data=json_results,
    hide_index=False)

df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
        "views_update": [[random.randint(0, 100) for _ in range(30)] for _ in range(3)],
    }
)
st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
        "views_update": st.column_config.BarChartColumn(
            "Updates", y_min=0, y_max=100
        ),
    },
    hide_index=True,
    use_container_width=True,
)
