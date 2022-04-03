from login_info import *
import requests
from jinja2 import Template
import urllib.parse
from jinja2 import Environment, FileSystemLoader


def render_url(query):
    return "https://query.wikidata.org/embed.html#" + urllib.parse.quote(query, safe="")


def generate_plant_html(collected_coins, qid, name, base_class="family"):
    collected_coins_query = get_collected_coins_query(collected_coins, qid, base_class)

    missing_coins_query = get_missing_coins_query(collected_coins, qid, base_class)

    page_template_path = "./docs/coin_by_group.html.jinja"
    with open(page_template_path) as f:
        page_template_string = f.read()

    page_template = Environment(loader=FileSystemLoader("docs/")).from_string(
        page_template_string
    )

    webpage = page_template.render(
        title=name,
        collected_coins_query=render_url(collected_coins_query),
        missing_coins_query=render_url(missing_coins_query),
    )

    if name == "all":
        webpage = page_template.render(
            title="All plant coins catalogued ",
            collected_coins_query=render_url(collected_coins_query),
            missing_coins_query=render_url(missing_coins_query),
        )
        with open(f"docs/{name.lower()}.html", "w") as f:
            f.write(webpage)
    else:
        with open(f"docs/{base_class}/{name.lower()}.html", "w") as f:
            f.write(webpage)


def get_collected_coins_query(collected_coins, qid, base_class):
    collected_coins_query_template_path = (
        f"./src/templates/collected_coins_by_{base_class}.rq.jinja"
    )

    with open(collected_coins_query_template_path) as f:
        collected_coins_query_template = Template(f.read())

    collected_coins_query = collected_coins_query_template.render(
        collected_coins=collected_coins, qid=qid
    )

    return collected_coins_query


def get_missing_coins_query(collected_coins, qid, base_class):
    missing_coins_query_template_path = (
        f"./src/templates/missing_coins_by_{base_class}.rq.jinja"
    )

    with open(missing_coins_query_template_path) as f:
        missing_coins_query_template = Template(f.read())

    missing_coins_query = missing_coins_query_template.render(
        collected_coins=collected_coins, qid=qid
    )

    return missing_coins_query
