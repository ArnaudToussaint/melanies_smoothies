# Import python packages
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from snowflake.snowpark.functions import col, when_matched

df = pd.DataFrame(np.random.randn(10, 20), columns=("col %d" % i for i in range(20)))

st.dataframe(df.style.highlight_max(axis=0))
