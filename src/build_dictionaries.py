from login_info import *
from helper import *
from wikidata2df import wikidata2df
import json
import time
import tqdm
from operator import itemgetter

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
?coin
?numista_id
?country ?countryLabel
?start_date
?face_value 
WITH {{
SELECT * WHERE {{
VALUES ?numista_id {{ "{joined_coins}" }}
?coin wdt:P10205 ?numista_id .
?coin wdt:P180 ?whatever .  
?coin wdt:P17 ?country . 
?coin wdt:P580 ?start_date . 
?coin wdt:P3934 ?face_value . 

?country rdfs:label ?countryLabel . 
FILTER ( LANG(?countryLabel) = "en" )

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
ORDER BY
  ?countryLabel
  ?start_date
  ?face_value
"""

df = wikidata2df(query)

valid_coins = list(df["numista_id"])
with open("data/coin_images.json") as f:
    coin_picture_dict_list = json.loads(f.read())

coins_present = [coin["id"] for coin in coin_picture_dict_list]

for i, row in tqdm.tqdm(df.iterrows()):

    coin = row["numista_id"]
    if coin in coins_present:
        continue
    response = requests.get(
        endpoint + "/coins/" + coin,
        headers={"Numista-API-Key": api_key},
    )
    coin_details = response.json()
    print(coin_details)
    coin_dict = {}
    coin_dict["face_value"] = float(row["face_value"])
    coin_dict["wikidata"] = row["coin"]
    coin_dict["country"] = row["countryLabel"]
    coin_dict["country_qid"] = row["country"]
    coin_dict["min_year"] = coin_details["min_year"]
    coin_dict["obverse"] = coin_details["obverse"]["thumbnail"]
    coin_dict["reverse"] = coin_details["reverse"]["thumbnail"]
    coin_dict["id"] = coin
    coin_dict["title"] = coin_details["title"]
    coin_picture_dict_list.append(coin_dict)
    coins_present.append(coin)
    time.sleep(0.1)


coin_picture_dict_list = sorted(
    coin_picture_dict_list, key=itemgetter("country", "min_year", "face_value")
)

with open("data/coin_images.json", "w+") as f:
    f.write(json.dumps(coin_picture_dict_list, indent=4, sort_keys=True))
