import json
import logging

import os
from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.ai.anomalydetector.models import DetectRequest, TimeSeriesPoint, TimeGranularity, \
    AnomalyDetectorError
from azure.core.credentials import AzureKeyCredential
import pandas as pd

import azure.functions as func

SUBSCRIPTION_KEY = os.environ["ANOMALY_DETECTOR_KEY"]
ANOMALY_DETECTOR_ENDPOINT = os.environ["ANOMALY_DETECTOR_ENDPOINT"]


def main(req: func.HttpRequest) -> func.HttpResponse:
    client = AnomalyDetectorClient(AzureKeyCredential(SUBSCRIPTION_KEY), ANOMALY_DETECTOR_ENDPOINT)

    series = []
    df = pd.read_csv(os.path.join("../data", "koala-survey-sightings-data.csv"), header=None, encoding='utf-8', parse_dates=[4])

    for _, row in df[['Date', 'HeightOfKoalaInTree_m']].iterrows():
        series.append(TimeSeriesPoint(timestamp=row[0], value=row[1]))

    request = DetectRequest(series=series, granularity=TimeGranularity.daily)
    
    try:
        response = client.detect_entire_series(request)
    except AnomalyDetectorError as e:
        msg = 'Error code: {} '.format(e.error.code) + 'Error message: {}'.format(e.error.message)
        logging.error(msg)
        return func.HttpResponse('Error code: {} '.format(e.error.code), status_code=500)
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(str(e), status_code=500)

    anomalies = []
    if any(response.is_anomaly):
        for i, value in enumerate(response.is_anomaly):
            if value:
                anomalies.append({'index': i, 'value': value})

    return func.HttpResponse(
            json.dumps(anomalies),
            status_code=200
    )
