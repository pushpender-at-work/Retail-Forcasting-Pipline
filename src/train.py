from sqlalchemy import create_engine
from dotenv import load_dotenv
import os 
import pandas as pd 
from prophet import Prophet
import pickle

load_dotenv()

engine=create_engine(url=os.getenv('DB_URL'))

stores=pd.read_sql("select distinct store_id from sales",engine)

for sid in stores['store_id']:
    
    df=pd.read_sql(f'SELECT ds, y FROM v_sales_for_prophet WHERE store_id={sid}', engine)
    

    if len(df)<2:
        continue

    prophet=Prophet(yearly_seasonality=True,weekly_seasonality=True)
    m=prophet.fit(df)

    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecast['store_id'] = sid
    
    forecast.to_sql('forecasts', engine, if_exists='append', index=False)
    print(f'forcast done {sid}')
    
    with open(f'models/prophet_store_{sid}.pkl', 'wb') as f:
        pickle.dump(m, f)
    
    print(f'Store {sid} done')

# for testing 
# forcast=pd.read_sql('select * from forecasts where store_id=1 LIMIT 31 ',engine)
# print(forcast)