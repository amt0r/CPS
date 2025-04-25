import unittest
from unittest.mock import MagicMock

import pandas as pd
import weather_preprocessing
from pymongo import MongoClient


class TestWeatherDataProcessing(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(MongoClient)
        self.mock_db = self.mock_client['weather']
        self.mock_collection = self.mock_db['monthly_avg_1941_2020']
        
        self.mock_csv_data = pd.DataFrame({
            'timestamp': ['19410101T0000', '19420101T0000'],
            'Basel Temperature [2 m elevation corrected]': [5.2, 3.8],
            'Basel Precipitation Total': [10.1, 12.2],
            'Basel Wind Gust': [15.0, 16.5]
        })
        
        pd.read_csv = MagicMock(return_value=self.mock_csv_data)
        
    def test_process_weather_data(self):
        processed_data = weather_preprocessing.process_weather_data("aga.csv")
        
        self.assertEqual(len(processed_data), 2)
        
        self.assertIn('timestamp', processed_data.columns)
        self.assertIn('Basel Temperature [2 m elevation corrected]', processed_data.columns)
        self.assertIn('Basel Precipitation Total', processed_data.columns)
        self.assertIn('Basel Wind Gust', processed_data.columns)
        
    def test_save_to_mongodb(self):
        weather_preprocessing.save_to_mongodb(self.mock_csv_data, self.mock_collection)
        
        self.mock_collection.insert_many.assert_called_once()

    def test_delete_collection(self):
        weather_preprocessing.delete_collection(self.mock_collection)
        
        self.mock_collection.drop.assert_called_once()

if __name__ == '__main__':
    unittest.main()
