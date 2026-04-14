import os
import requests
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    """
    Gets NASA api key from env variables
    """
    return  os.getenv("API_KEY")

def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")

def get_asteroid_data(start_date=None, end_date=None):
    api_key = get_api_key()
    url= "https://api.nasa.gov/neo/rest/v1/feed"

    if end_date is None:
        end_date = datetime.now()

    if start_date is None:
        start_date = end_date - timedelta(days=7)

    # Data validation
    if start_date > end_date:
        raise ValueError("start date must be before end date")

    if (end_date - start_date).days > 30:
        raise ValueError("Date range cannot exceed 30 days")
    
    all_data = []
    current_start = start_date

    # Paginate data 7 days at a time
    while current_start <= end_date:
        current_end = current_start + timedelta(days=6)

        if current_end > end_date:
            current_end = end_date

        params = {
            "start_date": format_date(current_start),
            "end_date": format_date(current_end),
            "api_key": api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            all_data.append(data)

            print(f"Fetched: {params['start_date']} to {params['end_date']}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        current_start = current_end + timedelta(days=1)

    # Write data to file
    return all_data


if __name__ == "__main__":
    get_asteroid_data()
