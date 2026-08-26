import pandas as pd

# Read the CSV files and concatenate them into a single DataFrame

df = pd.concat([
    pd.read_csv("data/2024-25.csv"),
    pd.read_csv("data/2025-26.csv")
], ignore_index=True)

df = df.sort_values(['element', 'GW']).reset_index(drop=True)
#the above sorts by players and gameweek, so that the data is in the correct order for each player

roll_cols = [
    'minutes', 'starts', 'goals_scored', 'assists', 'clean_sheets',
    'expected_goals', 'expected_assists', 'expected_goal_involvements',
    'expected_goals_conceded', 'creativity', 'threat', 'influence',
    'ict_index', 'bps', 'bonus', 'saves',
    'tackles', 'clearances_blocks_interceptions', 'recoveries', 'defensive_contribution'
]
#the above are the columns that we want to calculate rolling averages for

#we use a 4 gw rolling average for the above columns, recent points matter more than raw points across the season

for col in roll_cols:
    df[f'{col}_roll4'] = df.groupby('element')[col].transform(lambda x: x.shift(1).rolling(4, min_periods=1).mean())
    #the above calculates the rolling average for each player, shifting by 1 so that the current gameweek is not included in the average
    #new columns are created with the suffix _roll4 to indicate that they are rolling averages over the last 4 gameweeks, eg. goals_scored_roll4, assists_roll4, etc.
    #min_periods=1 is used so that if a player has played less than 4 gameweeks, the average is still calculated based on the available data

#static features, no rolling needed================================================================

static_cols = ['was_home', 'opponent_team', 'value', 'selected', 'position']

#if rolling features are all NaN, drop data, eg. gameweek 1
feature_cols = [f'{col}_roll4' for col in roll_cols] + static_cols

df_model = df.dropna(subset=[f'{col}_roll4' for col in roll_cols], how='all')

df_model=pd.get_dummies(df_model, columns=['position']) 
#converts positions into 0/1 categorical columns, eg. position_GK, position_DEF, position_MID, position_FWD

df_model['was_home'] = df_model['was_home'].astype(int) 
#the was_home column is a boolean, convert to int for modeling

position_cols = [c for c in df_model.columns if c.startswith('position_')]
feature_cols = [f'{col}_roll4' for col in roll_cols] + ['was_home', 'opponent_team', 'value', 'selected'] + position_cols
#position also included in feature_cols

X = df_model[feature_cols]
y = df_model['total_points']

print(X.shape)
print(y.describe())


