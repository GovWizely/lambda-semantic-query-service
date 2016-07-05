# Lambda Semantic Query Service

This project provides an AWS Lambda that maps a search query into controlled vocabulary filters and a fulltext query using 
the [ITA Taxonomy API](http://developer.trade.gov/ita-taxonomies.html).
The idea is to call this Lambda, probably via an AWS API Gateway, to pre-process a searcher's query in order to extract filter terms.

## Prerequisites

Follow instructions from [python-lambda](https://github.com/nficano/python-lambda) to ensure your basic development environment is ready,
including:

* Python
* Pip
* Virtualenv
* Virtualenvwrapper
* AWS credentials

Then make sure you have your [Trade.gov API Key](https://api.trade.gov) handy.

## Getting Started

	git clone git@github.com:loren/lambda-semantic-query-service.git
	cd lambda-semantic-query-service
	mkvirtualenv -r requirements.txt lambda-semantic-query-service

## Configuration

* Edit `service.py` and change the `API_KEY` to use your key
* Define AWS credentials in either `config.yaml` or in the [default] section of ~/.aws/credentials.
* Edit `event.json` if you want to change the test value for the query
* Edit `config.yaml` if you want to specify a different AWS region, role, and so on.
* Make sure you do not commit the API key or AWS credentials to version control

## Invocation

	lambda invoke -v

{'query': u'the and contracting in', 'filters': {'country': [u'United States'], 'world_region': [u'Oceania', u'Pacific Rim']}}

 
## Deploy

	lambda deploy
