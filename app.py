import streamlit as st
from my_pages import Home,SQL_Analytics, Crud_operations, Player_stats, Live_scores

st.set_page_config(
    page_title="Cricbuzz Cricket Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🏏 Cricket Dashboard")
page = st.sidebar.radio(
    "Choose a page",
    ["Home","SQL Analytics", "CRUD Operations", "Player Stats", "Live Scores"]
)
if page == "Home":
    Home.run()
elif page == "SQL Analytics":
    SQL_Analytics.run()
elif page == "CRUD Operations":
    Crud_operations.run()
elif page == "Player Stats":
    Player_stats.run()
elif page == "Live Scores":
    Live_scores.run()
