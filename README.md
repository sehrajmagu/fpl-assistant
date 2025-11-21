# FPL Assistant

FPL Assistant is a Streamlit-based web application that uses official Fantasy Premier League data to compare players, explore teams, and analyze useful statistics for decision-making.

## Features

1. Display top players based on total points, form, and other metrics.

2. Compare two players side-by-side with detailed stats such as goals, assists, clean sheets, ICT Index values, and price.

3. Browse players by team and view their upcoming fixture difficulty.

4. Automatically fetches live data from the FPL API (no private keys required).

## Project Structure
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

## Requirements

Python 3.10+

Streamlit

Pandas

Requests

## Future Plans

Recommendation system based on similar player profiles

## Notes

This project is intended for learning and experimentation. All data is publicly available through the official FPL API.
