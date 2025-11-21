import streamlit as st
import pandas as pd
from src.fpl_data import fetch_fpl_data
from src.style import load_css
load_css()
# Load data once
data = fetch_fpl_data()
players = pd.DataFrame(data["elements"])
teams_data = data["teams"]
teams = {t["id"]: t["name"] for t in teams_data}

# Add team names to player DF
players["team_name"] = players["team"].map(teams)

def get_player_stats(row):
    return {
        "Name": row["web_name"],
        "Team": row["team_name"],
        "Position": ["GK", "DEF", "MID", "FWD"][row["element_type"] - 1],
        "Price (£m)": row["now_cost"] / 10,
        "Total Points": row["total_points"],
        "PPG": row["points_per_game"],
        "Goals": row["goals_scored"],
        "Assists": row["assists"],
        "Clean Sheets": row["clean_sheets"],
        "ICT Index": row["ict_index"],
        "Threat": row["threat"],
        "Creativity": row["creativity"],
        "Influence": row["influence"],
    }

st.title("Compare Two Premier League Players")

st.markdown("Choose a team → then choose a player to compare their FPL stats.")

# --- TEAM SELECTION ---
team_list = sorted(list(teams.values()))

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Team for Player 1", team_list)
    p1_list = players[players["team_name"] == team1]["web_name"].sort_values()
    player1 = st.selectbox("Player 1", p1_list)

with col2:
    team2 = st.selectbox("Team for Player 2", team_list)
    p2_list = players[players["team_name"] == team2]["web_name"].sort_values()
    player2 = st.selectbox("Player 2", p2_list)

# --- DISPLAY RESULTS ---
p1_row = players[players["web_name"] == player1].iloc[0]
p2_row = players[players["web_name"] == player2].iloc[0]

p1_stats = get_player_stats(p1_row)
p2_stats = get_player_stats(p2_row)

df_compare = pd.DataFrame([p1_stats, p2_stats], index=["Player 1", "Player 2"])

st.dataframe(df_compare, use_container_width=True)
