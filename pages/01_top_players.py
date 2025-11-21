import streamlit as st
from src.fpl_data import get_top_players
from src.style import load_css
load_css()


st.set_page_config(page_title="FPL Assistant", page_icon="⚽", layout="wide")

st.title("Fantasy Premier League Assistant")

st.markdown("### Top-performing players in FPL right now (live data)")

with st.spinner("Fetching latest data..."):
    df = get_top_players(15)

# --- Display as Custom HTML Table ---
st.markdown(df.to_html(classes='styled-table', index=False, escape=False), unsafe_allow_html=True)


