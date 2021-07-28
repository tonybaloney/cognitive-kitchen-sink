import logging
import os
from datetime import datetime
from azure.core.exceptions import HttpResponseError
from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.ai.anomalydetector.models import DetectRequest, TimeSeriesPoint, TimeGranularity
from azure.core.credentials import AzureKeyCredential
import pandas as pd

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        client = AnomalyDetectorClient(AzureKeyCredential(os.environ["ANOMALY_DETECTOR_KEY"]), os.environ["ANOMALY_DETECTOR_ENDPOINT"])

        try:
            height_of_koala = int(req.params.get('height_of_koala'))
            height_of_tree = int(req.params.get('height_of_tree'))
            if height_of_tree == 0:
                raise ValueError
        except ValueError as e:
            logging.exception(e)
            return func.HttpResponse(str(e), status_code=500)

        df = pd.read_csv(os.path.join("data", "koala-survey-sightings-data.csv"), encoding='utf-8', parse_dates=[['Date', 'Time']])

        # Drop entries with no height recorded.
        df.dropna(subset=['HeightOfKoalaInTree_m', 'HeightOfTree_m'], inplace=True)
        # Drop entries recorded at the exact same time
        df.drop_duplicates(subset = ["Date_Time"], inplace=True)
        # Calculate the percentage of the tree the Koala has climbed
        df['PercentageHeightClimbed'] = df['HeightOfKoalaInTree_m'] / df['HeightOfTree_m']
        # Turn into a timeseries
        series = [TimeSeriesPoint(timestamp=row[0], value=row[1]) for _, row in df[['Date_Time', 'PercentageHeightClimbed']].sort_values(by=['Date_Time']).iterrows()]
        
        # Add the user input
        series.append(TimeSeriesPoint(timestamp=datetime.now(), value=height_of_koala/height_of_tree))
        request = DetectRequest(series=series, granularity=TimeGranularity.NONE)
    
        response = client.detect_last_point(request)
    except HttpResponseError as e:
        msg = 'Error code: {} '.format(e.error.code) + 'Error message: {}'.format(e.error.message)
        logging.error(msg)
        return func.HttpResponse('Error code: {} '.format(e.error.code), status_code=500)
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(str(e), status_code=500)

    if response.is_anomaly:
        return func.HttpResponse(
            "Anomaly",
            status_code=200
        )
    else:
        return func.HttpResponse(
            "OK",
            status_code=200
        )
