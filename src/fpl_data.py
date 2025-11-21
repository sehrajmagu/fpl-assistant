import requests
import pandas as pd

def fetch_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_fixtures():
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_team_mapping(teams_data):
    return {team['id']: team['short_name'] for team in teams_data}

def get_next_fixture(team_id, fixtures, teams):
    next_fix = "No fixture"
    for f in fixtures:
        if not f['finished']:
            if f['team_h'] == team_id:
                opp = teams.get(f['team_a'], "Unknown")
                diff = f.get('team_h_difficulty', '?')
                next_fix = f"vs {opp} (Diff {diff})"
                break
            elif f['team_a'] == team_id:
                opp = teams.get(f['team_h'], "Unknown")
                diff = f.get('team_a_difficulty', '?')
                next_fix = f"@ {opp} (Diff {diff})"
                break
    return next_fix

def get_top_players(top_n=15):
    data = fetch_fpl_data()
    fixtures = fetch_fixtures()
    players = data['elements']
    teams = get_team_mapping(data['teams'])

    table = []
    for p in players:
        next_fix = get_next_fixture(p['team'], fixtures, teams)
        table.append({
            "Name": f"{p['first_name']} {p['second_name']}",
            "Team": teams[p['team']],
            "Form": float(p['form']),
            "Total Points": p['total_points'],
            "Price": p['now_cost'] / 10,
            "Goals": p['goals_scored'],
            "Assists":p['assists'],
            "Clean Sheets": p['clean_sheets'],
            "Next Fixture": next_fix
        })

    df = pd.DataFrame(table).sort_values(by="Total Points", ascending=False).head(top_n)
    df.reset_index(drop=True, inplace=True)         # remove original index (the player ID)
    df.index += 1                                   # make index start at 1
    df.index.name = "Rank"                          # optional: name the index
    return df

def get_all_players():
    data = fetch_fpl_data()
    fixtures = fetch_fixtures()
    players = data['elements']
    teams = {t['id']: t['name'] for t in data['teams']}  # FULL team name here

    table = []
    for p in players:
        table.append({
            "Name": f"{p['first_name']} {p['second_name']}",
            "Team": teams[p['team']],  
            "Form": p['form'],
            "Total Points": p['total_points'],
            "Minutes": p['minutes'],
            "Goals":p['goals_scored'],
            "Assists":p['assists'],
            "Clean Sheets":p["clean_sheets"],
            "Price": p['now_cost'] / 10,
            #"Next Fixture": get_next_fixture(p['team'], fixtures, teams)
        })

    return pd.DataFrame(table)
