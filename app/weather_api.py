from typing import Optional
from pymongo import MongoClient
from .utils import validate_latitude, validate_longitude
import requests
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

class WeatherAPI:
    """
        This class provides methods to interact with a weather API and store
        retrieved data in MongoDB.

        Attributes:
            base_url (str): The base URL of the weather API.
            weather_params (str): Comma-separated list of weather parameters to retrieve.
            cache (dict): A dictionary to cache API responses.
            client (MongoClient): A MongoClient object for connecting to MongoDB.
            db (Database): A Database object representing the weather database.
            collection (Collection): A Collection object representing the historical weather data collection.
        """
    def __init__(self):
        """
            Initializes the WeatherAPI object. Sets up the base URL, weather parameters,
            cache, MongoDB connection, database, and collection.
                """
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.weather_params = "temperature_2m,wind_speed_10m,relativehumidity_2m"
        self.cache = {}  # cache to store weather data
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["weather_db"]
        self.collection = self.db["historical_data"]

    def get_user_location(self) -> Optional[tuple[float, float]]:
        """
            Prompts the user to enter their latitude and longitude. Validates the input
            and returns a tuple of (latitude, longitude) if valid, otherwise returns None.

            Returns:
            Optional[tuple[float, float]]: A tuple containing the user's latitude and longitude
                                                    if valid, otherwise None.
            """
        while True:
            latitude = input("Enter latitude: ")
            if validate_latitude(latitude):
                break
            else:
                print("Invalid latitude. Please enter a valid latitude.")

        while True:
            longitude = input("Enter longitude: ")
            if validate_longitude(longitude):
                break
            else:
                print("Invalid longitude. Please enter a valid longitude.")

        return float(latitude), float(longitude)

    def create_api_url(self, latitude: float, longitude: float, date: str) -> str:
        """
        Creates a URL for the weather API based on the provided latitude, longitude,and date.

            Args:
                    latitude (float): The user's latitude.
                    longitude (float): The user's longitude.
                    date (str): The date for which to retrieve weather data (YYYY-MM-DD format).

            Returns:
                    str: The complete URL for the weather API request.
                """
        return f"{self.base_url}?latitude={latitude}&longitude={longitude}&current={self.weather_params}&date={date}"

    def get_weather_data(self, url: str) -> Optional[dict]:
        """
            Fetches weather data from the provided URL using the weather API.

                - Checks the cache first. If the data exists in the cache, it retrieves it from there.
                - Otherwise, it makes an API call, retrieves the data, and stores it in the cache
                  for future use.

            Args:
                    url (str): The URL for the weather API request.

            Returns:
                    Optional[dict]: A dictionary containing the weather data if successful,
                                     otherwise None.
                """
        try:
            if url in self.cache:
                logging.info("Fetching weather data from cache")
                return self.cache[url]
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            self.cache[url] = data
            return data

        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred during API call: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            return None

    def fetch_historical_weather_data(self, start_date: str, end_date: str) -> Optional[list]:
        """
            Fetches historical weather data for the specified date range from a weather archive API."""
        latitude, longitude = self.get_user_location()
        try:
            #url = "https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
            #url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
            url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relativehumidity_2m,precipitation,rain,windgusts_10m"

            logging.info(f"Fetching historical weather data from URL: {url}")
            logging.info(f"Fetching historical weather data from URL: {url}")  # Log the URL
            response = requests.get(url)

            response.raise_for_status()
            data = response.json()
            return data['hourly'] if 'hourly' in data else None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred during API call: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            return None

    def store_historical_data(self, datalist) -> None:
        """
            Stores a list of historical weather data entries in the MongoDB collection.

            Args:
                datalist (list): A list of dictionaries containing historical weather data.

            Returns:
                None
            """
        try:
            # Insert historical weather data into MongoDB collection
            results=self.collection.insert_many(datalist)
            print(f"Inserted {len(results.inserted_ids)} records into collection: {self.collection}")


        except Exception as e:
            print(f"Error storing historical data in MongoDB : {e}")

    def get_historical_data(self, date: str) -> Optional[dict]:
        """
            Retrieves historical weather data for a specific date from the MongoDB collection.

            Args:
                date (str): The date for which to retrieve historical data (YYYY-MM-DD format).

            Returns:
                Optional[dict]: A dictionary containing the historical weather data for the given date
                                 if found, otherwise None.
            """
        try:
            # Retrieve historical weather data from MongoDB based on date
            result = self.collection.find({'date': date})
            datalist = list(result)
            if datalist:
                dataframe = pd.DataFrame(datalist)
                print(dataframe)
            else:
                print("No historical weather data found for the given date")

        except Exception as e:
            print(f"Error fetching historical data from MongoDB: {e}")

