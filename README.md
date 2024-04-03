 Weather Data App

This Python application retrieves and processes weather data using a weather API, optionally storing it in a MongoDB database.

## Features:

* Retrieves current weather data (temperature) for a specified location and date.
* Stores historical weather data (optional).

## Getting Started

### Prerequisites

* Python 3.x
* Requests library (`pip install requests`)
* Pandas library (`pip install pandas`)
* pymongo library (`pip install pymongo`)
* A weather API account (refer to the chosen API's documentation)
* MongoDB database (consider using a free tier service for local development)

### Usage

1. **Configure Weather API:** Update the `base_url` and `weather_params` variables in `weather_api.py` according to your chosen API's documentation. You might also need to replace the API endpoint URL in `fetch_historical_weather_data` based on the API.
2. **Set up MongoDB:** Replace the connection string (`mongodb://localhost:27017/`) in `weather_api.py` with your MongoDB connection details.
3. **Run the application:**

   ```bash
   python main.py
