import streamlit as st
import requests
from config import HEADERS

def run():
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