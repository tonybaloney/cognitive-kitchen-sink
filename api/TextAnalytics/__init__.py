import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import azure.functions as func
import json
from ..utils import debuggable


@debuggable()
def main(req: func.HttpRequest) -> func.HttpResponse: 
    species = req.params['species']
    with open('data/plants.json') as plants_index:
        plants = json.load(plants_index)

    if species not in plants:
        return func.HttpResponse(
            "Plant not recognized",
            status_code=400
        ) 

    plant_info = os.path.join('data', 'apni', plants[species]['id'] + '.txt')
    if not os.path.exists(plant_info):
        return func.HttpResponse(
            "No information on this plant",
            status_code=400
        )

    with open(plant_info) as p:
        plant_description = p.read()

    endpoint = os.environ["TEXT_ANALYTICS_ENDPOINT"]
    key = os.environ["TEXT_ANALYTICS_KEY"]

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    articles = [plant_description]
    results = []
    result = text_analytics_client.extract_key_phrases(articles)
    for _, doc in enumerate(result):
        if not doc.is_error:
            results.extend(doc.key_phrases)

    
    return func.HttpResponse(
            json.dumps({"text": plant_description, "key_phrases": results, "link": "https://bie.ala.org.au/species/https://id.biodiversity.org.au/node/apni/{0}#".format(plants[species]['id'])}),
            status_code=200
        ) 