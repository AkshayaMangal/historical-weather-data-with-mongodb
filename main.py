from app.weather_app import WeatherApp
import datetime
import pandas as pd

if __name__ == "__main__":
    app = WeatherApp()
    app.run()

    # Test fetching historical weather data
    start_date = "2022-06-01"
    end_date = "2022-08-05"
    historical_data = app.weather_api.fetch_historical_weather_data(start_date, end_date)

    if historical_data:
        if historical_data:
            print("Historical Weather Data:")
            print(historical_data)
            df = pd.DataFrame(historical_data)

            # Extract date from 'time' column
            df['date'] = pd.to_datetime(df['time'].str.split('T').str[0])
            print(df)
            # convert the Dataframe to list of Dictionaries
            data_to_insert = df.to_dict(orient='records')

            try:
                app.weather_api.store_historical_data(data_to_insert)
                print("Historical data stored successfully in MongoDB")
            except Exception as e:
                print(f"Error storing historical data in MongoDB: {e}")

            try:
                # Fetch data for a date in the format stored in MongoDB
                date_to_fetch = datetime.datetime(2022, 6, 1)  # Adjust the format as needed
                app.weather_api.get_historical_data(date_to_fetch)
            except Exception as e:
                print(f"Error fetching historical data from MongoDB: {e}")

    else:
        print("Failed to fetch historical weather data")