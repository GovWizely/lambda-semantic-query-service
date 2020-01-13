import vcr

from service import get_taxonomies_api_url, query_filter_mapping


def test_get_taxonomies_api_url():
    params_dict = {
        'q': 'the United States and pacific rim contracting in oceania malasia pacifico',
        'api_key': 'mykey',
        'types': 'World Regions,Countries'}
    expected_url = "https://api.trade.gov/ita_taxonomies/search?q=the+United+States+and+pacific" \
                   "+rim+contracting+in+oceania+malasia+pacifico&api_key=mykey" \
                   "&types=World+Regions%2CCountries"
    assert get_taxonomies_api_url(params_dict) == expected_url


@vcr.use_cassette()
def test_query_filter_mapping(monkeypatch):
    monkeypatch.setenv("TAXONOMIES_API_KEY", "mykey")
    q = "the United States and pacific rim contracting in oceania malasia pacifico cuba in scuba"
    result_dict = query_filter_mapping(q)
    expected_dict = {
        'filters': {
            'country': ['Cuba', 'United States'],
            'world_region': ['Oceania', 'Pacific Rim']
        },
        'query': 'the and contracting in malasia pacifico in scuba'
    }
    assert result_dict == expected_dict
