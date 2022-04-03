from login_info import *
from helper import *
from wikidata2df import wikidata2df
import json

endpoint = "https://api.numista.com/api/v2"
user_id = "231967"
response = requests.get(
    endpoint + "/users/" + user_id + "/collected_coins",
    params={"lang": "en"},
    headers={"Numista-API-Key": api_key},
)
user_details = response.json()
collected_coins = user_details["collected_coins"]

with open("data/coin_images.json") as f:
    coin_images = json.loads(f.read())

page_template_path = "./docs/all.html.jinja"
with open(page_template_path) as f:
    page_template_string = f.read()

page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
    page_template_string
)

webpage = page_template.render(coins=coin_images, title="All coins")

with open("docs/all.html", "w") as f:
    f.write(webpage)


with open("docs/index.html.jinja") as f:
    page_template_string = f.read()

page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
    page_template_string
)

webpage = page_template.render()

with open("docs/index.html", "w") as f:
    f.write(webpage)


# Render By Family pages

with open("src/queries/get_families.rq") as f:
    query = f.read()


families_df = wikidata2df(query)
print(families_df)
plant_families = []
seen = []
for i, row in families_df.iterrows():
    if row["family"] in seen:
        continue
    else:
        seen.append(row["family"])
    plant_families.append(
        {
            "lowercase_name": row["family_name"].lower(),
            "name": row["family_name"],
            "qid": row["family"],
            "pic_urls": row["pics"].split("|"),
        }
    )

print(plant_families)


with open("docs/family.html.jinja") as f:
    page_template_string = f.read()

page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
    page_template_string
)

webpage = page_template.render(plant_families=plant_families)

with open("docs/family.html", "w") as f:
    f.write(webpage)

for plant_family in plant_families:
    generate_plant_html(
        collected_coins,
        qid=plant_family["qid"],
        name=plant_family["name"],
        base_class="family",
    )

# Render By Country pages

with open("src/queries/get_countries.rq") as f:
    query = f.read()

countries_df = wikidata2df(query)
print(countries_df)
countries = []
seen = []
for i, row in countries_df.iterrows():
    if row["country"] in seen:
        continue
    else:
        seen.append(row["country"])
    countries.append(
        {
            "lowercase_name": row["countryLabel"].lower(),
            "name": row["countryLabel"],
            "qid": row["country"],
            "pic_urls": row["pics"].split("|"),
        }
    )

with open("docs/country.html.jinja") as f:
    page_template_string = f.read()
page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
    page_template_string
)
webpage = page_template.render(countries=countries)
print(webpage)
with open("docs/country.html", "w") as f:
    f.write(webpage)

with open("docs/family.html.jinja") as f:
    page_template_string = f.read()

page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
    page_template_string
)

webpage = page_template.render(plant_families=plant_families)

for country in countries:
    generate_plant_html(
        collected_coins,
        qid=country["qid"],
        name=country["name"],
        base_class="country",
    )
