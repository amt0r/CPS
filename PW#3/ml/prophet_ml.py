import pandas as pd
from prophet import Prophet
from pymongo import MongoClient

YEARS_FORECAST = 25

def fetch_data_from_mongodb(collection):
    return list(collection.find())

def prepare_data_for_prophet(data, key):
    return pd.DataFrame([{
        'ds': record['ds'],
        'y': record[key]
    } for record in data if key in record])

def forecast_with_prophet(df, periods=YEARS_FORECAST * 12):
    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=periods, freq='MS')
    forecast = model.predict(future)

    return forecast[['ds', 'yhat']]

def save_forecast_to_mongodb(forecast, collection):
    collection.delete_many({})

    forecast['ds'] = pd.to_datetime(forecast['ds'])
    forecast_dict = forecast.to_dict(orient='records')

    collection.insert_many(forecast_dict)

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client['weather']
    collection = db['monthly_avg_1941_2020']

    data = fetch_data_from_mongodb(collection)

    targets = ["temperature", "precipitation", "wind_gust"]

    combined_df = None

    for key in targets:
        df = prepare_data_for_prophet(data, key)
        forecast = forecast_with_prophet(df)
        forecast.rename(columns={'yhat': key}, inplace=True)

        if combined_df is None:
            combined_df = forecast
        else:
            combined_df = combined_df.merge(forecast, on='ds')

    save_forecast_to_mongodb(combined_df, db['forecast'])
    print("Forecast data saved to MongoDB.")

