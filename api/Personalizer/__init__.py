import logging
import os
from azure.cognitiveservices.personalizer import PersonalizerClient
from azure.cognitiveservices.personalizer.models import RankableAction, RewardRequest, RankRequest
from msrest.authentication import CognitiveServicesCredentials

import datetime, json, os, time, uuid
from azure.core.exceptions import HttpResponseError

import pandas as pd

import azure.functions as func


def get_actions():
    action1 = RankableAction(id='pasta', features=[{"taste":"salty", "spice_level":"medium"},{"nutrition_level":5,"cuisine":"italian"}])
    action2 = RankableAction(id='ice cream', features=[{"taste":"sweet", "spice_level":"none"}, { "nutritional_level": 2 }])
    action3 = RankableAction(id='juice', features=[{"taste":"sweet", 'spice_level':'none'}, {'nutritional_level': 5}, {'drink':True}])
    action4 = RankableAction(id='salad', features=[{'taste':'salty', 'spice_level':'none'},{'nutritional_level': 2}])
    return [action1, action2, action3, action4]


def get_user_timeofday():
    res={}
    time_features = ["morning", "afternoon", "evening", "night"]
    time = input("What time of day is it (enter number)? 1. morning 2. afternoon 3. evening 4. night\n")
    try:
        ptime = int(time)
        if(ptime<=0 or ptime>len(time_features)):
            raise IndexError
        res['time_of_day'] = time_features[ptime-1]
    except (ValueError, IndexError):
        print("Entered value is invalid. Setting feature value to", time_features[0] + ".")
        res['time_of_day'] = time_features[0]
    return res


def get_user_preference():
    res = {}
    taste_features = ['salty','sweet']
    pref = input("What type of food would you prefer? Enter number 1.salty 2.sweet\n")
    
    try:
        ppref = int(pref)
        if(ppref<=0 or ppref>len(taste_features)):
            raise IndexError
        res['taste_preference'] = taste_features[ppref-1]
    except (ValueError, IndexError):
        print("Entered value is invalid. Setting feature value to", taste_features[0]+ ".")
        res['taste_preference'] = taste_features[0]
    return res




def _main(req: func.HttpRequest) -> func.HttpResponse:
    client = PersonalizerClient(os.environ['PERSONALIZER_ENDPOINT'], CognitiveServicesCredentials(os.environ['PERSONALIZER_KEY']))
            
    keep_going = True
    while keep_going:

        eventid = str(uuid.uuid4())

        context = [get_user_preference(), get_user_timeofday()]
        actions = get_actions()

        rank_request = RankRequest( actions=actions, context_features=context, excluded_actions=['juice'], event_id=eventid)
        response = client.rank(rank_request=rank_request)
        
        print("Personalizer service ranked the actions with the probabilities listed below:")
        
        rankedList = response.ranking
        for ranked in rankedList:
            print(ranked.id, ':',ranked.probability)

        print("Personalizer thinks you would like to have", response.reward_action_id+".")
        answer = 'y'

        reward_val = "0.0"
        if(answer.lower()=='y'):
            reward_val = "1.0"
        elif(answer.lower()=='n'):
            reward_val = "0.0"
        else:
            print("Entered choice is invalid. Service assumes that you didn't like the recommended food choice.")

        client.events.reward(event_id=eventid, value=reward_val)

        keep_going = False
    return func.HttpResponse(
            "OK",
            status_code=200
        )    


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        return _main(req)
    except Exception:
        import os
        if os.getenv('DEBUG', True):
            import sys, traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exception_details = traceback.format_exception(exc_type, exc_value,
                                            exc_traceback)
            return func.HttpResponse(
                repr(exception_details),
                mimetype="text/plain",
                status_code=500
            )
        else:
            return func.HttpResponse(
                "Server Error",
                status_code=500
            )
