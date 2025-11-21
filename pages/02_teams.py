import streamlit as st
from src.fpl_data import get_all_players
from src.style import load_css


st.set_page_config(page_title="Teams", page_icon="🏟️", layout="wide")

load_css()  # SAME CSS AS MAIN PAGE

st.title("Team View (Full Squad Stats)")

with st.spinner("Loading all players..."):
    df = get_all_players()

teams = sorted(df["Team"].unique())

selected_team = st.selectbox("Select a Premier League team", teams)

team_df = df[df["Team"] == selected_team].sort_values(by="Total Points", ascending=False)


st.markdown(f"### {selected_team} — Full Squad \nNext Fixture: ")
st.dataframe(team_df, use_container_width=True)
