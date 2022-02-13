from login_info import *
import requests

endpoint = "https://api.numista.com/api/v2"

user_id = "231967"
response = requests.get(
    endpoint + "/users/" + user_id + "/collected_coins",
    params={"lang": "en"},
    headers={"Numista-API-Key": api_key},
)

print(response)
user_details = response.json()


print(user_details)
