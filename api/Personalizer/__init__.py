import json
import os
from azure.cognitiveservices.personalizer import PersonalizerClient
from azure.cognitiveservices.personalizer.models import RankableAction, RankRequest, RewardRequest
from msrest.authentication import CognitiveServicesCredentials

import os
import uuid

import pandas as pd

import azure.functions as func
from ..utils import debuggable

SHORTHANDS = {"E.": "Eucalyptus", 
         "L.":"Lophostemon",
         "C.": "Corymbia",
         "A.": "Angophora"}
TRAINING_MODE = False

def get_options(df: pd.DataFrame):
    options = []

    for n in df['TreeSpecies'].dropna().unique():
        family = n
        for k, v in SHORTHANDS:
            if n.startswith(k):
                family = v
        options.append(RankableAction(id=n, features=[{'tree_family': str(family), 'genus': 'Myrtaceae'},]))

    return options


def train(client, df, options):
    # Train the model , shouldn't do this every time
    for _, row in df.iterrows():
        eventid = str(uuid.uuid4())
        context = [{'area': row['SurveyArea']}, {'habitat': row['BushlandOrUrban']}]
        rank_request = RankRequest(actions=options, context_features=context, event_id=eventid)
        response = client.rank(rank_request=rank_request)
        if row['TreeSpecies'] not in response.ranking:
            reward = 0
        elif row['TreeSpecies'] == response.ranking[0]:
            reward = 1
        else:
            reward = 0.2
        print('worked out reward as ', reward)
        client.events.reward(event_id=eventid, value=reward)


@debuggable()
def main(req: func.HttpRequest) -> func.HttpResponse:
    client = PersonalizerClient(os.environ['PERSONALIZER_ENDPOINT'], CognitiveServicesCredentials(os.environ['PERSONALIZER_KEY']))

    df = pd.read_csv('data/koala-survey-sightings-data.csv', encoding='utf-8', parse_dates=[['Date', 'Time']])

    action = req.params.get('action', False)

    if not action:
        region = req.params['region']
        habitat = req.params['habitat']

        options = get_options(df)[:50]

        if TRAINING_MODE:
            train(client, df, options)

        # Get a recommendation for the current input
        eventid = str(uuid.uuid4())
        rank_request = RankRequest(actions=options, context_features=[{'area': region}, {'habitat': habitat}], event_id=eventid)
        response = client.rank(rank_request=rank_request)

        results = sorted([{'id': ranked.id, 'probability': ranked.probability} for ranked in response.ranking], key=lambda k: k['probability'], reverse=True) 

        return func.HttpResponse(
                json.dumps({"id": eventid, "recommendations": results}),
                status_code=200
            )
    elif action == 'choose':
        id = req.params['id']
        try:
            response = float(req.params['response'])
            client.events.reward(event_id=id, value=response)
        except ValueError:
            return func.HttpResponse(
                "bad response value",
                status_code=400
            )
    else:
        return func.HttpResponse(
                "invalid action",
                status_code=400
            )