from login_info import *
import requests
from jinja2 import Template
import urllib.parse
from jinja2 import Environment, FileSystemLoader


def render_url(query):
    return "https://query.wikidata.org/embed.html#" + urllib.parse.quote(query, safe="")


def generate_plant_html(collected_coins, family_qid, family_name, base_folder="/"):
    collected_coins_query_template_path = (
        "./src/templates/collected_coins_by_family.rq.jinja"
    )

    with open(collected_coins_query_template_path) as f:
        collected_coins_query_template = Template(f.read())

    collected_coins_query = collected_coins_query_template.render(
        collected_coins=collected_coins, family_qid=family_qid
    )

    missing_coins_query_template_path = (
        "./src/templates/missing_coins_by_family.rq.jinja"
    )

    with open(missing_coins_query_template_path) as f:
        missing_coins_query_template = Template(f.read())

    missing_coins_query = missing_coins_query_template.render(
        collected_coins=collected_coins, family_qid=family_qid
    )

    page_template_path = "./docs/coin_by_group.html.jinja"
    with open(page_template_path) as f:
        page_template_string = f.read()

    page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
        page_template_string
    )

    webpage = page_template.render(
        plant_family_name=all,
        collected_coins_query=render_url(collected_coins_query),
        missing_coins_query=render_url(missing_coins_query),
    )

    with open(f"docs{base_folder}{family_name.lower()}.html", "w") as f:
        f.write(webpage)
