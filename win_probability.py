#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
import json


def jstring(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Get data from the API
parameters = {
    "gameId": 401112435,
    "year": 2019
}
response = requests.get("https://api.collegefootballdata.com/lines", params=parameters)

# Import the data into a pandas DataFrame
json_str = jstring(response.json())
df = pd.read_json(json_str)

# explode the 4 line providers into their own rows
df = df.explode('lines')

df
