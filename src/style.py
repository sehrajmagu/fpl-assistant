import streamlit as st

def load_css():
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #38003c; 
            background-image: linear-gradient(180deg, #38003c 0%, #240028 100%);
            color: #ffffff;
        }

        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0);
        }

        [data-testid="stSidebar"] {
            background-color: #531a63;
            color: #ffffff;
        }

        .stMarkdown, .stText, h1, h2, h3, h4, h5 {
            color: #ffffff !important;
        }

        .stDataFrame {
            background-color: #531a63;
            border-radius: 12px !important;
        }

        div[data-testid="stImage"] img {
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
        }

        hr {
            border: 1px solid #9b59b6;
        }

        div.stButton > button:first-child {
            background-color: #00ff87 !important;
            color: black !important;
            border-radius: 10px !important;
            font-weight: bold !important;
            transition: 0.3s !important;
        }
        div.stButton > button:hover {
            background-color: #03c96b !important;
            color: black !important;
        }
    </style>
    """, unsafe_allow_html=True)
