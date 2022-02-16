from login_info import *
from helper import *


endpoint = "https://api.numista.com/api/v2"
user_id = "231967"
response = requests.get(
    endpoint + "/users/" + user_id + "/collected_coins",
    params={"lang": "en"},
    headers={"Numista-API-Key": api_key},
)
user_details = response.json()

collected_coins = user_details["collected_coins"]

generate_plant_html(collected_coins, family_qid="Q756", family_name="all")

generate_plant_html(
    collected_coins,
    family_qid="Q156569",
    family_name="Rubiaceae",
    base_folder="/family/",
)

with open("docs/index.html.jinja") as f:
    page_template_string = f.read()

page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
    page_template_string
)

webpage = page_template.render()

with open("docs/index.html", "w") as f:
    f.write(webpage)
