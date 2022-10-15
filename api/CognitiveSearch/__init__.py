import requests
import azure.functions as func
import os
from ..utils import debuggable
import json

@debuggable()
def main(req: func.HttpRequest) -> func.HttpResponse: 
    endpoint = os.getenv('COGNITIVE_SEARCH_ENDPOINT')
    index = os.getenv('COGNITIVE_SEARCH_INDEX')
    key = os.getenv('COGNITIVE_SEARCH_KEY')
    query = {  
        "answers": "extractive", 
        "featuresMode" : "enabled",
        "queryType": "semantic",
        "queryLanguage": "ja",
        "search": req.params['question'],  
        "top": 3
    }
    query_headers = {
        "api-key": key,
        "Content-Type": 'application/json'
    }
    response = requests.post(f'{endpoint}indexes/{index}/docs/search?api-version=2020-06-30-Preview', json=query, headers=query_headers)
    if not response.ok:
        return func.HttpResponse(body='search api error', status_code=500)
    results = response.json().get("@search.answers", [])
    return func.HttpResponse(json.dumps(results), status_code=200)
