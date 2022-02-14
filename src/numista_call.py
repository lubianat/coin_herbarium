from login_info import *
import requests
from jinja2 import Template
import urllib.parse


def render_url(query):
    return "https://query.wikidata.org/embed.html#" + urllib.parse.quote(query, safe="")


endpoint = "https://api.numista.com/api/v2"

user_id = "231967"
response = requests.get(
    endpoint + "/users/" + user_id + "/collected_coins",
    params={"lang": "en"},
    headers={"Numista-API-Key": api_key},
)

print(response)
user_details = response.json()

print([0])

collected_coins = user_details["collected_coins"]

collected_coins_query_template_path = "./src/templates/all_coins_to_fill.rq.jinja"

with open(collected_coins_query_template_path) as f:
    collected_coins_query_template = Template(f.read())

collected_coins_query = collected_coins_query_template.render(
    collected_coins=collected_coins
)

missing_coins_query_template_path = "./src/templates/missing_coins_to_fill.rq.jinja"

with open(missing_coins_query_template_path) as f:
    missing_coins_query_template = Template(f.read())

missing_coins_query = missing_coins_query_template.render(
    collected_coins=collected_coins
)


page_template_path = "./docs/index.html.jinja"


with open(page_template_path) as f:
    page_template = Template(f.read())


webpage = page_template.render(
    collected_coins_query=render_url(collected_coins_query),
    missing_coins_query=render_url(missing_coins_query),
)

with open("docs/index.html", "w") as f:
    f.write(webpage)
