import datetime 
import streamlit as st
import pandas as pd
import pymysql
import requests


# API 

PLAYER_SEARCH_URL = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
PLAYER_STATS_URL = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"
PLAYER_BATTING_URL = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/batting"
PLAYER_BOWLING_URL = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/bowling"

HEADERS = {
    "x-rapidapi-key": "d8ce6d3122mshd84847e1f215325p1db145jsnc5ecec004cfa",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}



# 1. Player Stats



elif page == "Player Stats":
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
                st.write("##### (TEST  ODI  T20I  T20)")
                st.dataframe(bat_df)

        # Bowling Stats
        bowl_res = requests.get(PLAYER_BOWLING_URL.format(player_id=player_id), headers=HEADERS)
        if bowl_res.status_code == 200:
            bowl_data = bowl_res.json()
            if "values" in bowl_data:
                bowling = bowl_data["values"]
                bowl_df = pd.DataFrame(bowling)
                st.write("#### 🎯 Bowling Stats (By Format)")
                st.write("##### (TEST  ODI  T20I  T20)")
                st.dataframe(bowl_df)


# 2. Live Scores


elif page == "Live Scores":
    st.title("🏏 Cricbuzz Live Match Dashboard")
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    headers = HEADERS

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error("Failed to fetch live scores.")
    else:
        data_1 = response.json()
        matches = []
        match_dict = {}

        # Collect all matches
        for match_type in data_1.get("typeMatches", []):
            for series in match_type.get("seriesMatches", []):
                series_data = series.get("seriesAdWrapper", {})
                series_name = series_data.get("seriesName")

                for match in series_data.get("matches", []):
                    info = match.get("matchInfo", {})
                    score = match.get("matchScore", {})

                    match_id = info.get("matchId")
                    team1 = info.get("team1", {}).get("teamName")
                    team2 = info.get("team2", {}).get("teamName")
                    match_desc = info.get("matchDesc")
                    match_format = info.get("matchFormat")
                    state = info.get("state")
                    status = info.get("status")
                    venue = info.get("venueInfo", {}).get("ground")
                    city = info.get("venueInfo", {}).get("city")

                    match_label = f"{team1} vs {team2} - {match_desc} ({state})"
                    matches.append(match_label)
                    match_dict[match_label] = {
                        "series": series_name,
                        "match_id": match_id,
                        "format": match_format,
                        "venue": venue,
                        "city": city,
                        "state": state,
                        "status": status,
                        "team1": team1,
                        "team2": team2,
                        "score": score
                    }

        # Sidebar dropdown
        selected_match = st.selectbox("🎯 Select a Match", matches)

        if selected_match:
            details = match_dict[selected_match]
            st.subheader(f"📌 {selected_match}")
            st.markdown(f"""
            - 🏆 **Series**: {details['series']}
            - 🏟 **Venue**: {details['venue']}
            - 🌆 **City**: {details['city']}
            - ⏳ **Format**: {details['format']}
            - 📢 **Status**: {details['status']}
            - 🔄 **State**: {details['state']}
            """)

            # Current Score
            st.subheader("📊 Current Score")
            score_data = details["score"]
            if score_data:
                if "team1Score" in score_data:
                    t1 = details["team1"]
                    scr1 = score_data["team1Score"].get("inngs1", {})
                    st.success(f"{t1}: {scr1.get('runs',0)}/{scr1.get('wickets',0)} ({scr1.get('overs',0)} overs)")

                if "team2Score" in score_data:
                    t2 = details["team2"]
                    scr2 = score_data["team2Score"].get("inngs1", {})
                    st.info(f"{t2}: {scr2.get('runs',0)}/{scr2.get('wickets',0)} ({scr2.get('overs',0)} overs)")
            else:
                st.warning("No live score available yet.")
   










