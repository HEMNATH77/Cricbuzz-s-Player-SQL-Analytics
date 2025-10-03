import streamlit as st
import pandas as pd
import requests
from config import HEADERS, PLAYER_SEARCH_URL, PLAYER_STATS_URL, PLAYER_BATTING_URL, PLAYER_BOWLING_URL

def run():
    st.title("📊 Cricbuzz Player Stats Dashboard")

    query = st.text_input("Enter Player Name")
    player_id = None
    player_name = None

    if st.button("Search Player") and query:
        res = requests.get(PLAYER_SEARCH_URL, headers=HEADERS, params={"plrN": query})
        if res.status_code == 200:
            data = res.json()
            if "player" in data and data["player"]:
                player_options = {p["name"]: p["id"] for p in data["player"]}
                player_name = st.selectbox("Select Player", list(player_options.keys()))
                if player_name:
                    player_id = player_options[player_name]

    if player_id:
        st.markdown(f"### 📌 {player_name} Stats")
        
        #career info

        
        info_res = requests.get(PLAYER_STATS_URL.format(player_id=player_id), headers=HEADERS)
        if info_res.status_code == 200:
            player_info = info_res.json()
            col1, col2 = st.columns([1, 3])
            with col2:
                st.markdown(f"**Name:** {player_info.get('name','N/A')}")
                st.markdown(f"**Country/Intl Team:** {player_info.get('intlTeam','N/A')}")
                st.markdown(f"**Teams:** {player_info.get('teams','N/A')}")
                st.markdown(f"**Role:** {player_info.get('role','N/A')}")
                st.markdown(f"**DOB:** {player_info.get('DoB','N/A')}")
                st.markdown(f"**Batting Style:** {player_info.get('bat','N/A')}")
                st.markdown(f"**Bowling Style:** {player_info.get('bowl','N/A')}")

            # Career Stats Summary

            if "careerStats" in player_info and player_info["careerStats"]:
                st.write("#### 🏆 Career Stats Summary")
                career_df = pd.DataFrame(player_info["careerStats"])
                st.dataframe(career_df)

        # Batting Stats
        bat_res = requests.get(PLAYER_BATTING_URL.format(player_id=player_id), headers=HEADERS)
        if bat_res.status_code == 200:
            bat_data = bat_res.json()
            if "values" in bat_data:
                batting = bat_data["values"] 
                bat_df = pd.DataFrame(batting)
                st.write("#### 🏏 Batting Stats (By Format)")
                st.write("##### (TEST  ODI  T20I  IPL)")
                st.dataframe(bat_df)

        # Bowling Stats
        bowl_res = requests.get(PLAYER_BOWLING_URL.format(player_id=player_id), headers=HEADERS)
        if bowl_res.status_code == 200:
            bowl_data = bowl_res.json()
            if "values" in bowl_data:
                bowling = bowl_data["values"]
                bowl_df = pd.DataFrame(bowling)
                st.write("#### 🎯 Bowling Stats (By Format)")
                st.write("##### (TEST  ODI  T20I  IPL)")
                st.dataframe(bowl_df)

