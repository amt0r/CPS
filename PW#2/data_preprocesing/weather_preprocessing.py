import pandas as pd
from pymongo import MongoClient

PATH_TO_CSV = "./PW#2/data/dataexport_20250410T232753.csv"

client = MongoClient("mongodb://localhost:27017/")
db = client['weather']
collection = db['monthly_avg_1941_2020']

def process_weather_data(csv_path):
    df = pd.read_csv(csv_path, skiprows=9)

    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%dT%H%M')

    df['month'] = df['timestamp'].dt.to_period('M')

    df_monthly = df.groupby('month').mean().reset_index()

    df_monthly['timestamp'] = df_monthly['month'].dt.to_timestamp()

    df_monthly.drop(columns='month', inplace=True)

    return df_monthly


def delete_collection(collection):
    collection.drop()

def save_to_mongodb(dataframe, collection):
    column_map = {
        'timestamp': 'ds',
        'Basel Temperature [2 m elevation corrected]': 'temperature',
        'Basel Precipitation Total': 'precipitation',
        'Basel Wind Gust': 'wind_gust'
    }
    
    dataframe.rename(columns=column_map, inplace=True)

    dataframe.reset_index(drop=True, inplace=True)

    data_dict = dataframe.to_dict(orient='records')
    collection.insert_many(data_dict)



if __name__ == "__main__":
    processed_data = process_weather_data(PATH_TO_CSV)
    
    delete_collection(collection)
    
    save_to_mongodb(processed_data, collection)
    
    print("Data saved to MongoDB.")
