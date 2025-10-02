import streamlit as st

def run():
    # Gradient Title
    st.markdown("""
        <h1 style='text-align: center; 
                   background: linear-gradient(90deg, blue,pink); 
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-size: 45px;'>
            🏏 Cricbuzz Cricket Dashboard
        </h1>
    """, unsafe_allow_html=True)

    # Subtitle
    st.markdown("""
        <div style="text-align: center; font-size:18px; padding:10px; color:#ccc;">
            🚀 Welcome to your interactive cricket analytics dashboard!  
            Get live updates, explore stats, and manage records with ease.
        </div>
        <br>
    """, unsafe_allow_html=True)

    # Two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="background: rgba(0, 123, 255, 0.1); 
                        padding:20px; 
                        border-radius:12px; 
                        border: 1px solid rgba(0,123,255,0.3);
                        box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
                <h3 style="color:#00aaff;">📌 Available Sections</h3>
                <ul style="font-size:16px; line-height:1.8; color:#eee;">
                    <li>📊 <b>SQL Analytics</b> → Run predefined SQL queries</li>
                    <li>🛠 <b>CRUD Operations</b> → Manage player records</li>
                    <li>📈 <b>Player Stats</b> → Search & view player profiles</li>
                    <li>🏟 <b>Live Scores</b> → Get real-time cricket updates</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="background: rgba(255, 193, 7, 0.1); 
                        padding:20px; 
                        border-radius:12px; 
                        border: 1px solid rgba(255,193,7,0.3);
                        box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
                <h3 style="color:#ffc107;">🔧 Tech Stack</h3>
                <ul style="font-size:16px; line-height:1.8; color:#eee;">
                    <li>🐍 <b>Python + Streamlit</b> → Web app</li>
                    <li>🗄 <b>MySQL</b> → Storage</li>
                    <li>📡 <b>Cricbuzz API</b> → Live cricket data</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive info box
    st.success("👉 Use the **sidebar** to navigate between sections and explore cricket insights!")

    # Footer
    st.markdown("""
        <hr>
        <div style="text-align: center; font-size:14px; color:grey;">
            Turning coffee into insights forever...🤍
        </div>
    """, unsafe_allow_html=True)
