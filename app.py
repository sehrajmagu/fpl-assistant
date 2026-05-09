from flask import Flask, render_template, request, jsonify
from src.fpl_data import get_top_players, get_all_players, fetch_fpl_data
import pandas as pd

app = Flask(__name__)


_cache = {} #self defined cache dictionary

def get_data():  
    if 'data' not in _cache:
        _cache['data'] = fetch_fpl_data()
    return _cache['data']

def get_players_df():
    if 'players_df' not in _cache:
        _cache['players_df'] = get_all_players()
    return _cache['players_df']

'''if we've never fetched the data before:
    go get it from the API and store it
return whatever is stored'''
# ── Pages ──────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/top-players')
def top_players():
    df = get_top_players(15)
    return render_template('top_players.html', table=df.to_dict(orient='records'), enumerate=enumerate)

@app.route('/team')
def team():
    df = get_players_df()
    teams = sorted(df['Team'].unique())
    return render_template('team.html', teams=teams)

@app.route('/compare')
def compare():
    data = get_data()
    teams = sorted({t['name'] for t in data['teams']})
    return render_template('compare.html', teams=teams)

@app.route('/captain')
def captain():
    return render_template('captain.html')

# ── API endpoints (called by JS in the templates) ──────

@app.route('/team-data')
def team_data():
    team = request.args.get('team', '')
    df = get_players_df()
    team_df = df[df['Team'] == team].sort_values('Total Points', ascending=False).drop(columns=['Team'])
    return jsonify(team_df.to_dict(orient='records'))

@app.route('/players-by-team')
def players_by_team():
    team = request.args.get('team', '')
    data = get_data()
    players = pd.DataFrame(data['elements'])
    teams = {t['id']: t['name'] for t in data['teams']}
    players['team_name'] = players['team'].map(teams)
    filtered = players[players['team_name'] == team]['web_name'].sort_values()
    return jsonify(filtered.tolist())

@app.route('/compare-data')
def compare_data():
    p1_name = request.args.get('p1', '')
    p2_name = request.args.get('p2', '')
    data = get_data()
    players = pd.DataFrame(data['elements'])
    teams = {t['id']: t['name'] for t in data['teams']}
    players['team_name'] = players['team'].map(teams)

    def get_stats(name):
        row = players[players['web_name'] == name].iloc[0]
        return {
            'Name': str(row['web_name']),
            'Team': str(row['team_name']),
            'Price (£m)': float(row['now_cost'] / 10),
            'Total Points': int(row['total_points']),
            'PPG': str(row['points_per_game']),
            'Goals': int(row['goals_scored']),
            'Assists': int(row['assists']),
            'Clean Sheets': int(row['clean_sheets']),
            'ICT Index': str(row['ict_index']),
            'Threat': str(row['threat']),
            'Creativity': str(row['creativity']),
            'Influence': str(row['influence']),
        }

    return jsonify({'stats': [get_stats(p1_name), get_stats(p2_name)]})

@app.route('/all-players-json')
def all_players_json():
    data = get_data()
    players = pd.DataFrame(data['elements'])
    teams = {t['id']: t['name'] for t in data['teams']}
    position_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}
    players['Team'] = players['team'].map(teams)
    players['Position'] = players['element_type'].map(position_map)
    result = players[['web_name', 'Team', 'Position', 'form', 'total_points',
                       'expected_goal_involvements', 'status']].copy()
    result.columns = ['web_name', 'Team', 'Position', 'form', 'total_points', 'xGI', 'status']
    return jsonify(result.to_dict(orient='records'))

@app.route('/get-captain', methods=['POST'])
def get_captain():
    body = request.get_json()
    selected = body.get('players', [])

    data = get_data()
    players_df = pd.DataFrame(data['elements'])
    player_lookup = {p['web_name']: p for p in data['elements']}

    def normalise(value, max_value):
        try: value = float(value)
        except: value = 0.0
        return min(value / max_value, 1)

    def fixture_modifier(is_home): return 1 if is_home else -1

    def score_player(p, position):
        form = normalise(p.get('form', 0), 10)
        pts = normalise(p.get('total_points', 0), 200)
        xgi = normalise(p.get('expected_goal_involvements', 0), 5)
        fix = fixture_modifier(True)  # placeholder until fixture logic added

        if position == 'FWD':
            return xgi * 45 + form * 30 + pts * 15 + fix * 10 + 3
        elif position == 'MID':
            return xgi * 40 + form * 30 + pts * 15 + fix * 10 + 3
        elif position == 'DEF':
            return form * 30 + pts * 20 + xgi * 15 + fix * 10
        elif position == 'GK':
            return form * 40 + pts * 30 + fix * 10 - 5
        return 0

    best_name, best_score, best_pos = None, -1, None

    for s in selected:
        name = s['name']
        pos = s['pos']
        raw = player_lookup.get(name)
        if not raw: continue
        if raw.get('status') != 'a': continue

        sc = score_player(raw, pos)
        if sc > best_score:
            best_score = sc
            best_name = name
            best_pos = pos

    return jsonify({'name': best_name, 'position': best_pos, 'score': round(best_score, 2)})

if __name__ == '__main__':
    app.run(debug=True)