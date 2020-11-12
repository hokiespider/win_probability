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

def sign(x):
  return 1-(x<=0)


# Get data from the API
df = pd.DataFrame()
for x in range(2013, 2021, 1):    # Line data is only available 2013+
    parameters = {
        "conference": "ACC",
        "year": x
    }
    response = requests.get("https://api.collegefootballdata.com/lines", params=parameters)

    # Import the data into a pandas DataFrame
    json_str = jstring(response.json())
    temp = pd.read_json(json_str)
    df = df.append(temp)

# explode the 4 line providers into their own rows
#df = df.explode('lines')

# Add Win/Loss column
school = "Virginia Tech"
home_games = df.query('homeTeam == @school')
home_games['score_diff'] = home_games['homeScore'] - home_games['awayScore']
home_games['home_away'] = "Home"
home_games.loc[home_games['score_diff'] > 0, 'wins'] = 1
home_games.loc[home_games['score_diff'] < 0, 'losses'] = 1

away_games = df.query('awayTeam == @school')
df.info()
away_games['score_diff'] = away_games['awayScore'] - away_games['homeScore']
away_games['home_away'] = "away"
away_games.sample()
away_games.loc[away_games['score_diff'] > 0, 'wins'] = 1

away_games.loc[away_games['score_diff'] < 0, 'losses'] = 1

df2 = home_games.append(away_games)

records = df.groupby(['season'])['wins', 'losses'].sum()
records
