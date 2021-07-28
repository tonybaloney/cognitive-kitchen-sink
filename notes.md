```python
df = pd.read_csv(os.path.join("../data", "koala-survey-sightings-data.csv"), encoding='utf-8', parse_dates=[['Date', 'Time']])
series = [TimeSeriesPoint(timestamp=row[0], value=row[1]) for _, row in df[['Date_Time', 'HeightOfKoalaInTree_m']].iterrows()]
```

```
[2021-07-28T07:03:53.679Z] Unable to serialize value: '18/11/2010 12:55:00' as type: 'iso-8601'., ISO8601Error: ISO 8601 time designator 'T' missing. Unable to parse datetime string '18/11/2010 12:55:00'
[2021-07-28T07:03:53.679Z] Traceback (most recent call last):
[2021-07-28T07:03:53.679Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/isodate/isodatetime.py", line 51, in parse_datetime
[2021-07-28T07:03:53.679Z]     datestring, timestring = datetimestring.split('T')
[2021-07-28T07:03:53.679Z] ValueError: not enough values to unpack (expected 2, got 1)
[2021-07-28T07:03:53.679Z] 
[2021-07-28T07:03:53.679Z] During handling of the above exception, another exception occurred:
[2021-07-28T07:03:53.679Z] 
[2021-07-28T07:03:53.679Z] Traceback (most recent call last):
[2021-07-28T07:03:53.679Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 765, in serialize_data
[2021-07-28T07:03:53.679Z]     return self.serialize_type[data_type](data, **kwargs)
[2021-07-28T07:03:53.679Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 1112, in serialize_iso
[2021-07-28T07:03:53.679Z]     attr = isodate.parse_datetime(attr)
[2021-07-28T07:03:53.679Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/isodate/isodatetime.py", line 53, in parse_datetime
[2021-07-28T07:03:53.679Z]     raise ISO8601Error("ISO 8601 time designator 'T' missing. Unable to"
[2021-07-28T07:03:53.679Z] isodate.isoerror.ISO8601Error: ISO 8601 time designator 'T' missing. Unable to parse datetime string '18/11/2010 12:55:00'
[2021-07-28T07:03:53.679Z] 
[2021-07-28T07:03:53.679Z] During handling of the above exception, another exception occurred:
[2021-07-28T07:03:53.679Z] 
[2021-07-28T07:03:53.679Z] Traceback (most recent call last):
[2021-07-28T07:03:53.679Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/api/AnomalyDetection/__init__.py", line 23, in main
[2021-07-28T07:03:53.680Z]     response = client.detect_entire_series(request)
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/azure/ai/anomalydetector/operations/_anomaly_detector_client_operations.py", line 71, in detect_entire_series
[2021-07-28T07:03:53.680Z]     body_content = self._serialize.body(body, 'DetectRequest')
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 629, in body
[2021-07-28T07:03:53.680Z]     return self._serialize(data, data_type, **kwargs)
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 483, in _serialize
[2021-07-28T07:03:53.680Z]     return self.serialize_data(
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 783, in serialize_data
[2021-07-28T07:03:53.680Z]     return self._serialize(data, **kwargs)
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 523, in _serialize
[2021-07-28T07:03:53.680Z]     new_attr = self.serialize_data(orig_attr, attr_desc['type'], **kwargs)
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 775, in serialize_data
[2021-07-28T07:03:53.680Z]     return self.serialize_type[iter_type](
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 860, in serialize_iter
[2021-07-28T07:03:53.680Z]     serialized.append(self.serialize_data(d, iter_type, **kwargs))
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 783, in serialize_data
[2021-07-28T07:03:53.680Z]     return self._serialize(data, **kwargs)
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 523, in _serialize
[2021-07-28T07:03:53.680Z]     new_attr = self.serialize_data(orig_attr, attr_desc['type'], **kwargs)
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 780, in serialize_data
[2021-07-28T07:03:53.680Z]     raise_with_traceback(
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/exceptions.py", line 51, in raise_with_traceback
[2021-07-28T07:03:53.680Z]     raise error.with_traceback(exc_traceback)
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 765, in serialize_data
[2021-07-28T07:03:53.680Z]     return self.serialize_type[data_type](data, **kwargs)
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/msrest/serialization.py", line 1112, in serialize_iso
[2021-07-28T07:03:53.680Z]     attr = isodate.parse_datetime(attr)
[2021-07-28T07:03:53.680Z]   File "/Users/anthonyshaw/projects/cognitive-kitchen-sink/.venv/lib/python3.8/site-packages/isodate/isodatetime.py", line 53, in parse_datetime
[2021-07-28T07:03:53.680Z]     raise ISO8601Error("ISO 8601 time designator 'T' missing. Unable to"
[2021-07-28T07:03:53.680Z] msrest.exceptions.SerializationError: Unable to serialize value: '18/11/2010 12:55:00' as type: 'iso-8601'., ISO8601Error: ISO 8601 time designator 'T' missing. Unable to parse datetime string '18/11/2010 12:55:00'

```