#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
import json


# Get data from the API
df = pd.DataFrame()
for x in range(2013, 2020, 1):    # Line data is only available 2013+
    parameters = {
        "team": "Virginia Tech",
        "year": x
    }
    response = requests.get("https://api.collegefootballdata.com/lines", params=parameters)

    # Import the data into a pandas DataFrame
    temp = pd.DataFrame(response.json()) # Create a DataFrame with a lines column that contains JSON
    # need to fill NA line lists for 2020
    temp = temp.explode('lines') # Explode the DataFrame so that each line gets its own row
    temp = temp.reset_index(drop=True) # After explosion, the indices are all the same - this resets them so that you can align the DataFrame below cleanly

    lines_df = pd.DataFrame(temp.lines.tolist()) # A separate lines DataFrame created from the lines JSON column
    temp = pd.concat([temp, lines_df], axis=1) # Concatenating the two DataFrames along the vertical axis.

    df = df.append(temp)
df = df[df.provider == 'consensus']
school = "Virginia Tech"

# explode the 4 line providers into their own rows
#df = df.explode('lines')



# Add Win/Loss column

df['score_diff'] = df['homeScore'] - df['awayScore']
df.loc[]


home_games = df[df.homeTeam == school]
home_games['score_diff'] = home_games['homeScore'] - home_games['awayScore']
home_games['home_away'] = "Home"
home_games.loc[home_games['score_diff'] > 0, 'wins'] = 1
home_games.loc[home_games['score_diff'] < 0, 'losses'] = 1

away_games = df.query('awayTeam == @school')
away_games['score_diff'] = away_games['awayScore'] - away_games['homeScore']
away_games['home_away'] = "away"
away_games.sample()
away_games.loc[away_games['score_diff'] > 0, 'wins'] = 1

away_games.loc[away_games['score_diff'] < 0, 'losses'] = 1

df2 = home_games.append(away_games)

records = df.groupby(['season'])['wins', 'losses'].sum()
records
