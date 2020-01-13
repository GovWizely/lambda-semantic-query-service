import os
import re
from urllib.parse import quote_plus, urlencode

import requests

BASE_URL = "https://api.trade.gov/ita_taxonomies/search"
LABEL_DICT = {'World Regions': 'world_region', 'Countries': 'country'}


def get_taxonomies_api_url(params_dict):
    return "?".join([BASE_URL, urlencode(params_dict, quote_via=quote_plus)])


def generate_tuples(parsed_json):
    for result in parsed_json['results']:
        for taxonomy_type in result['type']:
            if taxonomy_type in LABEL_DICT:
                yield result['label'], taxonomy_type


def query_filter_mapping(query_string):
    params_dict = {'q': query_string,
                   'api_key': os.getenv("TAXONOMIES_API_KEY"),
                   'types': ",".join(LABEL_DICT)}
    mapping_dict = {}

    url = get_taxonomies_api_url(params_dict)
    response = requests.get(url)
    parsed_json = response.json()
    for label, taxonomy_type in generate_tuples(parsed_json):
        reduced_query_string = re.sub(r"(?i)\b%s\b" % label, '', query_string)
        if reduced_query_string != query_string:
            query_string = reduced_query_string
            label_set = mapping_dict.setdefault(LABEL_DICT[taxonomy_type], set())
            label_set.add(label)

    for label, label_set in mapping_dict.items():
        mapping_dict[label] = sorted(list(label_set))
    result_dict = dict(filters=mapping_dict, query=" ".join(query_string.split()))
    return result_dict


def handler(event, context):
    return query_filter_mapping(event.get('q'))
