# -*- coding: utf-8 -*-

import json
import re
import requests
import urllib
from retrying import retry

API_KEY='YOUR_API_TRADE_GOV_KEY_HERE'

LABEL_DICT = {'World Regions': 'world_region', 'Countries': 'country_name'}
BASE_URL = "https://api.trade.gov/ita_taxonomies/search"


@retry(stop_max_attempt_number=5, wait_fixed=3000)
def query_filter_mapping(query_string, label_dict):
    params_dict = {'q': query_string, 'api_key': API_KEY, 'types': ",".join(label_dict.keys())}
    mapping_dict = {}
    url = "?".join([BASE_URL, urllib.urlencode(params_dict)])
    response = requests.get(url)
    parsed_json = response.json()
    for result in parsed_json['results']:
        for type in result['type']:
            reduced_query_string = re.sub(r"(?i)\b%s\b" % result['label'], '', query_string)
            if reduced_query_string != query_string:
                query_string = reduced_query_string
                label_set = mapping_dict.setdefault(label_dict[type], set())
                label_set.add(result['label'])

    for label, label_set in mapping_dict.iteritems():
        mapping_dict[label] = sorted(list(label_set))
    result_dict = dict(filters=mapping_dict, query=" ".join(query_string.split()))
    return result_dict


def handler(raw_event, context):
    event = {key: raw_event[key] for key in raw_event if raw_event[key] and raw_event[key] != ""}
    label_dict = {}
    label_dict['World Regions'] = event.get('world_region_label', LABEL_DICT['World Regions'])
    label_dict['Countries'] = event.get('country_name_label', LABEL_DICT['Countries'])
    return query_filter_mapping(event.get('q'), label_dict)
