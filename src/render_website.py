from login_info import *
from helper import *
from wikidata2df import wikidata2df
import json
from pathlib import Path

HERE = Path(__file__).parent.resolve()


def main():
    data_path = HERE.parents[0] / "data"
    docs_path = HERE.parents[0] / "docs"
    queries_path = HERE / "queries"

    endpoint = "https://api.numista.com/api/v2"
    user_id = "231967"
    response = requests.get(
        endpoint + "/users/" + user_id + "/collected_coins",
        params={"lang": "en"},
        headers={"Numista-API-Key": api_key},
    )
    user_details = response.json()
    collected_coins = user_details["collected_coins"]

    coin_images_path = data_path / "coin_images.json"
    coin_images = json.loads(coin_images_path.read_text())

    p = docs_path / "all.html.jinja"
    page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
        p.read_text()
    )

    webpage = page_template.render(coins=coin_images, title="All coins")

    p = docs_path / "all.html"
    p.write_text(webpage)

    p = docs_path / "index.html.jinja"
    page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
        p.read_text()
    )

    webpage = page_template.render()

    p = docs_path / "index.html"
    p.write_text(webpage)

    # Render By Family pages

    p = queries_path / "get_families.rq"
    query = p.read_text()
    families_df = wikidata2df(query)

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

    p = docs_path / "family.html.jinja"
    page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
        p.read_text()
    )
    webpage = page_template.render(plant_families=plant_families)

    p = docs_path / "family.html"
    p.write_text(webpage)

    for plant_family in plant_families:
        generate_plant_html(
            collected_coins,
            qid=plant_family["qid"],
            name=plant_family["name"],
            base_class="family",
        )

    # Render By Country pages
    p = queries_path / "get_countries.rq"
    query = p.read_text()

    countries_df = wikidata2df(query)
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

    p = docs_path / "country.html.jinja"
    page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
        p.read_text()
    )
    webpage = page_template.render(countries=countries)
    p = docs_path / "country.html"
    p.write_text(webpage)

    p = docs_path / "country.html.jinja"
    page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
        p.read_text()
    )
    webpage = page_template.render(plant_families=plant_families)

    for country in countries:
        generate_plant_html(
            collected_coins,
            qid=country["qid"],
            name=country["name"],
            base_class="country",
        )


if __name__ == "__main__":
    main()
