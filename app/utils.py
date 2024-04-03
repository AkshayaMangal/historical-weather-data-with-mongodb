# utils.py
import datetime

def validate_latitude(latitude: str) -> bool:
    """
       Validates a latitude value.

       A valid latitude must be a number between -90 and 90 (inclusive).

       Args:
           latitude (str): The latitude value to validate.

       Returns:
           bool: True if the latitude is valid, False otherwise.
       """
    try:
        float(latitude)
        return -90 <= float(latitude) <= 90
    except ValueError:
        return False


def validate_longitude(longitude: str) -> bool:
    """
        Validates a longitude value.

        A valid longitude must be a number between -180 and 180 (inclusive).

        Args:
            longitude (str): The longitude value to validate.

        Returns:
            bool: True if the longitude is valid, False otherwise.
        """
    try:
        float(longitude)
        return -180 <= float(longitude) <= 180
    except ValueError:
        return False

def validate_date(self, date: str) -> bool:
    """
        Validates a date string in YYYY-MM-DD format.

        Args:
            date (str): The date string to validate.

        Returns:
            bool: True if the date is valid, False otherwise.
        """
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
