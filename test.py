# Import python packages
import streamlit as st # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
import requests # type: ignore
import json
from snowflake.snowpark.functions import col, when_matched # type: ignore

df = pd.DataFrame(np.random.randn(10, 20), columns=("col %d" % i for i in range(20)))

st.dataframe(df.style.highlight_max(axis=0))
