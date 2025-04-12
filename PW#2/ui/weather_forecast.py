import sys
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pymongo import MongoClient
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def fetch_data(collection, date_filter=None):
    query = {}
    if date_filter:
        query = {"ds": {"$gte": date_filter['start'], "$lte": date_filter['end']}}
    return list(collection.find(query))

def plot_graphs(data, title_prefix=""):
    df = pd.DataFrame(data)
    df['ds'] = pd.to_datetime(df['ds'])

    fig, ax = plt.subplots(3, 1, figsize=(10, 15))

    ax[0].plot(df['ds'], df['temperature'], label='Temperature', color='red')
    ax[0].set_title(f'{title_prefix}Temperature')
    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('°C')
    ax[0].grid(True)

    ax[1].plot(df['ds'], df['precipitation'], label='Precipitation', color='blue')
    ax[1].set_title(f'{title_prefix}Precipitation')
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel('mm')
    ax[1].grid(True)

    ax[2].plot(df['ds'], df['wind_gust'], label='Wind Gust', color='green')
    ax[2].set_title(f'{title_prefix}Wind Gust')
    ax[2].set_xlabel('Date')
    ax[2].set_ylabel('km/h')
    ax[2].grid(True)

    plt.tight_layout()
    plt.show()

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client['weather']

        self.setWindowTitle("Weather")
        self.setGeometry(100, 100, 200, 100)

        layout = QVBoxLayout()

        self.btn_all_forecast = QPushButton("Forecast")
        self.btn_forecast_range = QPushButton("Forecast 2021-2025")
        self.btn_monthly_avg = QPushButton("Data 2021-2025")

        self.model_accuracy_label = QLabel("Model accuracy: ")
        self.calculate_accuracy()

        self.btn_all_forecast.clicked.connect(self.plot_forecast)
        self.btn_forecast_range.clicked.connect(self.plot_forecast_2021_2024)
        self.btn_monthly_avg.clicked.connect(self.plot_data_2021_2024)

        layout.addWidget(self.model_accuracy_label)
        layout.addWidget(self.btn_all_forecast)
        layout.addWidget(self.btn_forecast_range)
        layout.addWidget(self.btn_monthly_avg)

        self.setLayout(layout)

    def plot_forecast(self):
        data = fetch_data(self.db['forecast'])
        plot_graphs(data, title_prefix="Forecast – ")

    def plot_forecast_2021_2024(self):
        forecast_data = fetch_data(self.db['forecast'], date_filter={"start": datetime(2021, 1, 1), "end": datetime(2024, 12, 31)})
        plot_graphs(forecast_data, title_prefix="Forecast (2021-2025) – ")

    def plot_data_2021_2024(self):
        data = fetch_data(self.db['monthly_avg_2021_2024'])
        plot_graphs(data, title_prefix="Data – ")
        
    def calculate_accuracy(self):
        forecast_data = fetch_data(self.db['forecast'], date_filter={"start": datetime(2021, 1, 1), "end": datetime(2024, 12, 31)})
        data = fetch_data(self.db['monthly_avg_2021_2024'])
        
        predicted = [item['temperature'] for item in forecast_data]

        actual = [item['temperature'] for item in data]
        
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mae = mean_absolute_error(actual, predicted)
        r2 = r2_score(actual, predicted)
        
        self.model_accuracy_label.setText(f"Model accuracy: RMSE={rmse:.2f}, MAE={mae:.2f}, R²={r2:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
