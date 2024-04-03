import unittest
from weather_api import WeatherAPI

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.weather_api = WeatherAPI()

    def test_valid_input(self):
        start_date = "2022-06-01"
        end_date = "2022-08-05"
        historical_data = self.weather_api.fetch_historical_weather_data(start_date, end_date)
        self.assertIsNotNone(historical_data)
        self.assertIsInstance(historical_data, list)

    def test_invalid_latitude(self):
        start_date = "2022-06-01"
        end_date = "2022-08-05"
        latitude = "invalid_latitude"
        longitude = "50.0"  # Valid longitude for testing
        historical_data = self.weather_api.fetch_historical_weather_data(start_date, end_date)
        self.assertIsNone(historical_data)

    def test_invalid_longitude(self):
        start_date = "2022-06-01"
        end_date = "2022-08-05"
        latitude = "40.0"  # Valid latitude for testing
        longitude = "invalid_longitude"
        historical_data = self.weather_api.fetch_historical_weather_data(start_date, end_date)
        self.assertIsNone(historical_data)

if __name__ == "__main__":
    unittest.main()
