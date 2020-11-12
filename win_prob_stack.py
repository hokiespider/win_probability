import pandas as pd
import requests

params = {
    "team": "Virginia Tech",
    "year": 2019,
}

r = requests.get("https://api.collegefootballdata.com/lines", params=params)

df = pd.DataFrame(r.json()) # Create a DataFrame with a lines column that contains JSON
df = df.explode('lines') # Explode the DataFrame so that each line gets its own row
df = df.reset_index(drop=True) # After explosion, the indices are all the same - this resets them so that you can align the DataFrame below cleanly


lines_df = pd.DataFrame(df.lines.tolist()) # A separate lines DataFrame created from the lines JSON column
df = pd.concat([df, lines_df], axis=1) # Concatenating the two DataFrames along the vertical axis.

# Now you can filter down to whichever rows you need.
df = df[df.provider == 'consensus']

df
