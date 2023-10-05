import requests
from datetime import datetime

# When you see the comment 'PYOD' it means 'Provide your own data'

# All about Nutritionix API:
NUTRITIONIX_BASE_ENDPOINT = "https://trackapi.nutritionix.com"
APP_ID = ""  # PYOD
APP_KEY = ""  # PYOD

# All about Sheety API:
MY_SHEET_TOKEN = ""  # PYOD
MY_SHEET_ENDPOINT = ""  # PYOD
MY_SHEET_PAGE_NAME = ""  # PYOD


def get_current_datetime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%m/%d/%y")
    return current_time, current_date


def discover_exercises_stats():
    exercises = input("Tell me which exercises you did: ")
    exercise_endpoint = f"{NUTRITIONIX_BASE_ENDPOINT}/v2/natural/exercise"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY
    }
    parameters = {
        "query": exercises
    }
    response = requests.post(url=exercise_endpoint, headers=headers, json=parameters)
    return response.json()


exercises_stats_data = discover_exercises_stats()
print(exercises_stats_data)

datetime_of_user_input = get_current_datetime()

list_of_exercises_stats = exercises_stats_data["exercises"]

list_of_row_contents = []

for each_dict in list_of_exercises_stats:
    row_content = {
        MY_SHEET_PAGE_NAME: {
            "date": datetime_of_user_input[1],
            "time": datetime_of_user_input[0],
            "exercise": each_dict["name"],
            "duration": each_dict["duration_min"],
            "calories": each_dict["nf_calories"]
        }
    }
    list_of_row_contents.append(row_content)


def create_a_row_in_sheet(content: dict):
    headers = {
        "Authorization": MY_SHEET_TOKEN
    }
    response = requests.post(url=MY_SHEET_ENDPOINT, headers=headers, json=content)
    return response.text


for row_content in list_of_row_contents:
    create_a_row_in_sheet(row_content)
