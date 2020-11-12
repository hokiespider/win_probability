#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
import json

# What school are you analyzing?
school = "Virginia Tech"

# Get data from the API
df = pd.DataFrame()
for x in range(2013, 2020, 1):    # Line data is only available 2013+
    parameters = {
        "team": school,
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
df['spread'] = df.spread.astype('float')

# Add Win/Loss columns
home_games = df[df.homeTeam == school].copy()
home_games['score_diff'] = home_games['homeScore'] - home_games['awayScore']
home_games['home_away'] = "Home"
home_games.loc[home_games['score_diff'] > 0, 'wins'] = 1
home_games.loc[home_games['score_diff'] < 0, 'losses'] = 1

away_games = df[df.awayTeam == school].copy()
away_games['score_diff'] = away_games['awayScore'] - away_games['homeScore']
away_games['home_away'] = "away"
away_games.loc[away_games['score_diff'] > 0, 'wins'] = 1
away_games.loc[away_games['score_diff'] < 0, 'losses'] = 1
away_games['spread'] = away_games['spread'] * -1

df = home_games.append(away_games)

#records = df.groupby(['season'])['wins', 'losses'].sum()

# Import the odds of winning
filename = '/Users/appleuser/Documents/win_probability/odds_of_winning_lines.csv'
odds = pd.read_csv(filename)
odds = odds.melt(id_vars='Spread', value_vars=['Favorite', 'Underdog'], var_name='Type', value_name="Expected Wins")
odds.loc[odds['Spread'] == '20+', 'Spread'] = 20
odds['Spread'] = odds.Spread.astype('float')

odds.loc[odds['Type'] == "Favorite", 'Spread'] = odds['Spread'] * -1
df.loc[df['spread'] >= 20, 'spread'] = 20
df.loc[df['spread'] <= -20, 'spread'] = -20

df = df.merge(odds, how='left', left_on='spread', right_on='Spread')

df.loc[df['spread'] < 0, 'spread_group'] = '3. 0.5-6.5 Favorites'
df.loc[df['spread'] < -6.5, 'spread_group'] = '2. 7-14 Favorites'
df.loc[df['spread'] < -13.5, 'spread_group'] = ' 1. 14+ Favorites'
df.loc[df['spread'] == 0, 'spread_group'] = '4. pick-em'
df.loc[df['spread'] > 0, 'spread_group'] = '5. 0.5-6.5 Dogs'
df.loc[df['spread'] > 6.5, 'spread_group'] = '6. 7-14 Dogs'
df.loc[df['spread'] > 13.5, 'spread_group'] = '7. 14+ Dogs'
df.loc[df['season'] >= 2016, 'Coach'] = 'Fuente 2016-2019'
df.loc[df['season'] < 2016, 'Coach'] = 'Beamer 2013 - 2015'

groups = df.groupby(['Coach', 'spread_group'])['wins', 'losses', 'Expected Wins'].sum().round(2)
groups['win_perc'] = groups.apply(lambda x: x['wins'] / (x['wins'] + x['losses']), axis=1).round(2)
groups['wins vs expectation'] = groups['wins'] - groups['Expected Wins'].round(2)
groups
groups.to_clipboard()

coaches = df.groupby(['Coach'])['wins', 'losses', 'Expected Wins'].sum().round(2)
coaches['win_perc'] = coaches.apply(lambda x: x['wins'] / (x['wins'] + x['losses']), axis=1).round(2)
coaches['wins vs expectation'] = coaches['wins'] - coaches['Expected Wins'].round(2)
coaches
