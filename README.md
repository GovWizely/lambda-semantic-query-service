[![CircleCI](https://circleci.com/gh/GovWizely/lambda-semantic-query-service.svg?style=svg)](https://circleci.com/gh/GovWizely/lambda-semantic-query-service)

# Semantic Query Service

AWS Lambda mapping a search query into controlled vocabulary filters and a fulltext query using ITA Taxonomy API. 

Example query: _the United States and pacific rim contracting in oceania malasia pacifico cuba in scuba_

response:

```python
{
    'filters': {
        'country': ['Cuba', 'United States'],
        'world_region': ['Oceania', 'Pacific Rim']
    },
    'query': 'the and contracting in malasia pacifico in scuba'
}
```

## Prerequisites

- This project is tested against Python 3.7+ in [CircleCI](https://app.circleci.com/github/GovWizely/lambda-semantic-query-service/pipelines).
- Make sure you have your [Trade.gov API Key](https://api.trade.gov) handy.

### Local Development

```bash
git clone git@github.com:GovWizely/lambda-semantic-query-service.git
cd lambda-semantic-query-service
mkvirtualenv -p /usr/local/bin/python3.8 -r requirements-test.txt lambda-semantic-query-service
```


If you are using PyCharm, make sure you enable code compatibility inspections for Python 3.7/3.8.

### Tests

```bash
python -m pytest
```

## Configuration

* Define the Taxonomies API key as an environment variable `export TAXONOMIES_API_KEY=your_key`.
* Define AWS credentials in either `config.yaml` or in the [default] section of `~/.aws/credentials`. To use another profile, you can do something like `export AWS_DEFAULT_PROFILE=govwizely`.
* Edit `config.yaml` if you want to specify a different AWS region, role, and so on.
* Make sure you do not commit the AWS credentials to version control.

## Invocation

	lambda invoke -v
 
## Deploy
    
In the AWS Lambda console, set up the `TAXONOMIES_API_KEY` environment variable. Then you are ready to deploy:

	lambda deploy --requirements requirements.txt
