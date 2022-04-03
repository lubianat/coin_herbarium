from login_info import *
from helper import *
from wikidata2df import wikidata2df
import json
import time
import tqdm

endpoint = "https://api.numista.com/api/v2"
user_id = "231967"
response = requests.get(
    endpoint + "/users/" + user_id + "/collected_coins",
    params={"lang": "en"},
    headers={"Numista-API-Key": api_key},
)
user_details = response.json()
collected_coins = user_details["collected_coins"]

coins = list(set([str(coin["coin"]["id"]) for coin in collected_coins]))

joined_coins = '""'.join(coins)

qid = "Q756"
query = f"""
SELECT DISTINCT 
?numista_id
?whatever 
WITH {{
SELECT * WHERE {{
VALUES ?numista_id {{ "{joined_coins}" }}
?coin wdt:P10205 ?numista_id .
?coin wdt:P180 ?whatever .  
{{?whatever wdt:P31 wd:Q16521 . }}
UNION
{{?whatever wdt:P31 wd:Q55983715 . }}
}} 
}}
AS %results 
WHERE {{
  INCLUDE %results
   ?whatever wdt:P171* wd:{qid} .
   hint:Prior hint:gearing "forward".
}}
"""

print(query)
df = wikidata2df(query)

print(df)

valid_coins = list(df["numista_id"])

coin_picture_dict_list = []
for coin in tqdm.tqdm(valid_coins):
    response = requests.get(
        endpoint + "/coins/" + coin,
        headers={"Numista-API-Key": api_key},
    )
    coin_details = response.json()
    coin_dict = {}
    coin_dict["obverse"] = coin_details["obverse"]["picture"]
    coin_dict["reverse"] = coin_details["reverse"]["picture"]
    coin_dict["id"] = coin
    coin_dict["title"] = coin_details["title"]
    coin_picture_dict_list.append(coin_dict)
    time.sleep(0.1)

with open("data/coin_images.json", "w+") as f:
    f.write(json.dumps(coin_picture_dict_list, indent=4, sort_keys=True))
