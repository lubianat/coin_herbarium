from login_info import *
from helper import *
from wikidata2df import wikidata2df

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
        family_qid=plant_family["qid"],
        family_name=plant_family["name"],
        base_folder="/family/",
    )
