import logging
from .weather_api import WeatherAPI
from typing import Optional
logging.basicConfig(level=logging.INFO)

class WeatherApp:
    """
        This class represents a weather application that retrieves and processes weather data
        using a WeatherAPI object.

        Attributes:
            weather_api (WeatherAPI): An instance of the WeatherAPI class used to interact with the weather API.
        """

    def __init__(self):
        """
        Initializes the WeatherApp object by creating an instance of the WeatherAPI class.
                """
        self.weather_api = WeatherAPI()

    def get_user_input(self) -> str:
        """
        Prompts the user to enter a date in YYYY-MM-DD format and returns the entered date as a string.

        Returns:
                str: The date entered by the user.
                """
        return input("Enter date (YYYY-MM-DD): ")

    def process_weather_data(self, weather_data:Optional[dict]):
        """
        Processes the retrieved weather data.

        - If weather data is retrieved successfully, it logs a message and prints the current temperature.
        - If weather data retrieval fails, it logs a warning message.

        Args:
         weather_data (Optional[dict]): A dictionary containing the retrieved weather data, or None if retrieval fails.
                                                    """
        if weather_data:
            logging.info("Weather data retrieved successfully")
            print(f"  -Current Temperature (2m) : {weather_data['current']['temperature_2m']}C")
            print(f"  -Hourly Data (available ,not shown here for brevity")
        else:
            logging.warning("Failed to retrieve weather data")

    def run(self):
        """
        The main function of the weather application.

                1. Gets the user's location (latitude and longitude) using the WeatherAPI object.
                2. Prompts the user to enter a date.
                3. Creates the API URL for the weather data using the user's location and entered date.
                4. Logs a message indicating that weather data is being fetched.
                5. Retrieves weather data from the API using the WeatherAPI object.
                6. Processes the retrieved weather data using the process_weather_data function.
                7. In case of any exceptions, logs an error message.
                """
        try:
            latitude, logitude = self.weather_api.get_user_location()
            date = self.get_user_input()
            api_url = self.weather_api.create_api_url(latitude, logitude, date)
            logging.info(f"Fetching weather data for {date}...")
            weather_data = self.weather_api.get_weather_data(api_url)
            self.process_weather_data(weather_data)

        except Exception as e:
            logging.error(f"An error occurred : {str(e)}")