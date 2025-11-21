import streamlit as st
from src.style import load_css

load_css()

st.title("⚽ FPL Assistant")
st.markdown("""
Welcome to your personal **Fantasy Premier League analytics dashboard**.

Use the pages on the left to:
- 📊 View the top-performing players  
- 🏟️ See players by team  
- ⚔️ Compare two players side-by-side  

More features coming soon!
""")
