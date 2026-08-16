import pandas as pd 
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv('DB_URL'))


train_df=pd.read_csv('./data/train.csv',parse_dates=['Date'])
store_df=pd.read_csv('./data/store.csv')

store_df.columns=store_df.columns.str.lower()
train_df.columns=train_df.columns.str.lower()

store_df['competitiondistance']=store_df['competitiondistance'].fillna(value=store_df['competitiondistance'].median())

# train table with all open store data 
new_train_df=train_df[train_df['open']==1]

# making table columns 
sales=new_train_df[['store','date','sales','customers','open']].rename(columns={
    'store':'store_id'
})

stores=store_df[['store', 'storetype', 'assortment', 'competitiondistance']].rename(columns={
    'store':'store_id',
    'storetype':'store_type',
    'competitiondistance': 'competition_distance'
})

dates = new_train_df[['date', 'dayofweek', 'stateholiday', 'schoolholiday']].drop_duplicates(subset='date').rename(columns={
    'date': 'date_id',
    'dayofweek': 'day_of_week',
    'stateholiday': 'is_holiday',
    'schoolholiday': 'school_holiday'
})

sales.to_sql('sales',engine,if_exists='replace',index=False)
stores.to_sql('stores',engine,if_exists='replace',index=False)
dates.to_sql('dates',engine,if_exists='replace',index=False)

print('done!!')




