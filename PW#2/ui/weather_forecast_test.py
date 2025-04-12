import unittest
from datetime import datetime
from unittest.mock import MagicMock

import weather_forecast


class TestWeatherApp(unittest.TestCase):

    def setUp(self):
        self.mock_collection = MagicMock()
        self.mock_data = [
            {"ds": datetime(2021, 1, 1), "temperature": 10, "precipitation": 5, "wind_gust": 15},
            {"ds": datetime(2053, 1, 2), "temperature": 12, "precipitation": 3, "wind_gust": 20}
        ]
        self.mock_collection.find.return_value = self.mock_data
        
        def mock_find(query):
            start = query.get("ds", {}).get("$gte")
            end = query.get("ds", {}).get("$lte")
            return [item for item in self.mock_data if (start is None or item['ds'] >= start) and (end is None or item['ds'] <= end)]
        
        self.mock_collection.find = MagicMock(side_effect=mock_find)

    def test_fetch_data_with_date_filter(self):
        date_filter = {"start": datetime(2021, 1, 1), "end": datetime(2022, 12, 31)}

        data = weather_forecast.fetch_data(self.mock_collection, date_filter)

        self.assertEqual(len(data), 1)

    def test_fetch_data_without_date_filter(self):
        data = weather_forecast.fetch_data(self.mock_collection)

        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]["temperature"], 10)
        self.assertEqual(data[1]["temperature"], 12)

if __name__ == "__main__":
    unittest.main()
