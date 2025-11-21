FPL Assistant

FPL Assistant is a Streamlit-based web application that uses official Fantasy Premier League data to compare players, explore teams, and analyze useful statistics for decision-making.

Features

Display top players based on total points, form, and other metrics.

Compare two players side-by-side with detailed stats such as goals, assists, clean sheets, ICT Index values, and price.

Browse players by team and view their upcoming fixture difficulty.

Automatically fetches live data from the FPL API (no private keys required).

Project Structure
fpl-assistant/
│
├── app.py                  Main page (Top players)
├── pages/
│   ├── 02_teams.py         Team-based player view
│   └── 03_compare.py       Player comparison page
│
├── src/
│   ├── fpl_data.py         Fetches data from FPL API
│   └── style.py            Custom stylesheet
│
└── data/                   Optional storage or caching

Requirements

Python 3.10+

Streamlit

Pandas

Requests

Setup and Running Locally
git clone https://github.com/<your-username>/fpl-assistant.git
cd fpl-assistant

pip install -r requirements.txt
streamlit run app.py

Future Plans

Add visual charts for comparison

Enhanced search and filtering

Recommendation system based on similar player profiles

Notes

This project is intended for learning and experimentation. All data is publicly available through the official FPL API.
