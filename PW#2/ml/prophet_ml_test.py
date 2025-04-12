import unittest
from unittest.mock import MagicMock

import prophet_ml
from pymongo import MongoClient


class TestWeatherForecast(unittest.TestCase):
    
    def setUp(self):
        self.mock_client = MagicMock(MongoClient)
        self.mock_db = self.mock_client['weather']
        self.mock_collection = self.mock_db['monthly_avg_1941_2020']
        self.mock_forecast_collection = self.mock_db['forecast']
        
        self.mock_data = [
            {'ds': '2020-01-01', 'temperature': 5.2, 'precipitation': 10.1, 'wind_gust': 15.0},
            {'ds': '2020-02-01', 'temperature': 4.8, 'precipitation': 12.2, 'wind_gust': 16.5}
        ]
        self.mock_collection.find = MagicMock(return_value=self.mock_data)
        
    def test_fetch_data_from_mongodb(self):
        data = prophet_ml.fetch_data_from_mongodb(self.mock_collection)
        self.assertEqual(len(data), 2)
        self.assertIn('ds', data[0])
        self.assertIn('temperature', data[0])
        self.assertIn('precipitation', data[0])
        self.assertIn('wind_gust', data[0])

    def test_prepare_data_for_prophet(self):
        data = prophet_ml.fetch_data_from_mongodb(self.mock_collection)
        df = prophet_ml.prepare_data_for_prophet(data, 'temperature')
        self.assertEqual(df.shape[0], 2)
        self.assertIn('ds', df.columns)
        self.assertIn('y', df.columns)

    def test_forecast_with_prophet(self):
        data = prophet_ml.fetch_data_from_mongodb(self.mock_collection)
        df = prophet_ml.prepare_data_for_prophet(data, 'temperature')
        forecast = prophet_ml.forecast_with_prophet(df)
        self.assertEqual(forecast.shape[0], prophet_ml.YEARS_FORECAST * 12 + len(df))
        self.assertIn('ds', forecast.columns)
        self.assertIn('yhat', forecast.columns)

    def test_save_forecast_to_mongodb(self):
        data = prophet_ml.fetch_data_from_mongodb(self.mock_collection)
        df = prophet_ml.prepare_data_for_prophet(data, 'temperature')
        forecast = prophet_ml.forecast_with_prophet(df)
        
        prophet_ml.save_forecast_to_mongodb(forecast, self.mock_forecast_collection)
        
        self.mock_forecast_collection.insert_many.assert_called_once()
    
if __name__ == '__main__':
    unittest.main()
