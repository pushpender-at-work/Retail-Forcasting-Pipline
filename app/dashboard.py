import streamlit as st
from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv
import pandas as pd 

load_dotenv()
engine=create_engine(os.getenv('DB_URL'))

st.set_page_config(page_title="Sales Forecast", layout='wide')
st.title("Rossmann Sales Forecast Dashboard")
st.divider()

store_type=pd.read_sql('select distinct(store_type) from stores order by store_type',engine)
selected_store_type=st.sidebar.selectbox('Select Store Type',store_type['store_type'])
stores=pd.read_sql(f"select distinct store_id from stores where store_type='{selected_store_type}' order by store_id",engine)
selected_store=st.sidebar.selectbox('Select Store',stores['store_id'])


forecast_df = pd.read_sql(
    f"SELECT ds, yhat, yhat_lower, yhat_upper FROM forecasts WHERE store_id={selected_store} ORDER BY ds limit 30",
    engine
)

forecast_df = forecast_df.rename(columns={
    'ds': 'Date',
    'yhat': 'Predicted Sales',
    'yhat_lower': 'Lower Bound',
    'yhat_upper': 'Upper Bound'
})

st.subheader(f"Store {selected_store} ({selected_store_type}) - 30 Day Forecast")

col1,col2=st.columns(2)
with col1:
    with st.container(border=True,):
        st.write("Prediction Chart")
        st.line_chart(data=forecast_df.set_index('Date')[['Predicted Sales', 'Lower Bound', 'Upper Bound']],height=200)
with col2:
    
    st.dataframe(forecast_df)


st.divider()


st.write("### KPI Cards")
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.metric("Avg Sales", f"€{forecast_df['Predicted Sales'].mean():.0f}")

with col2:
    with st.container(border=True):
        st.metric("Max Forecast", f"€{forecast_df['Predicted Sales'].max():.0f}")

with col3:
    with st.container(border=True):
        st.metric("Min Forecast", f"€{forecast_df['Predicted Sales'].min():.0f}")