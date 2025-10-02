import streamlit as st
import pandas as pd
from db import connect_pymysql

def run():
    st.title("🛠️ CRUD Operations with MySQL")
    conn = connect_pymysql()
    cursor = conn.cursor()

    crud_option = st.sidebar.radio("Select Operation", ["Create", "Read", "Update", "Delete"])
    
    # Create
    if crud_option == "Create":
        st.subheader("Add a New Player")

        with st.form("create_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                player_id = st.number_input("Player Id", min_value=1)
                name = st.text_input("Batsman Name")
                matches = st.number_input("Matches Played", min_value=0)
            with col2:
                innings = st.number_input("Total Innings", min_value=0)
                runs = st.number_input("Runs", min_value=0)
                average = st.number_input("Average", min_value=0.0, format="%.2f")

            submitted = st.form_submit_button("Insert")
            if submitted:
                try:
                    cursor.execute(
                        "INSERT INTO records(player_id, player_name, matches, innings, runs, average) VALUES (%s,%s,%s,%s,%s,%s)",
                        (player_id, name, matches, innings, runs, average)
                    )
                    conn.commit()
                    st.success(f"🎉 Player **{name}** added successfully!")
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")

    # Read 

    elif crud_option == "Read":
        st.subheader("All Players in Records")

        cursor.execute("SELECT * FROM records")
        result = cursor.fetchall()
        if result:
            import pandas as pd
            df = pd.DataFrame(result, columns=["Player ID", "Name", "Matches", "Innings", "Runs", "Average"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No records found.")

    # Update
    elif crud_option == "Update":
        st.subheader("Update Player Info")

        player_id = st.number_input("Enter Player ID to Update", min_value=1)

        # Fetch Record
        if st.button("🔍 Fetch Record"):
            cursor.execute("SELECT * FROM records WHERE player_id=%s", (player_id,))
            record = cursor.fetchone()
            if record:
                st.session_state['record'] = record   # ✅ save to session state
            else:
                st.warning("⚠️ Player ID not found.")
                st.session_state.pop('record', None)

    # Show update form only if record exists
        if 'record' in st.session_state:
            record = st.session_state['record']   # ✅ use persisted record
            st.write("Editing:", record)

            with st.form("update_form"):
                name = st.text_input("Batsman Name", value=record[1])
                matches = st.number_input("Matches", min_value=0, value=record[2])
                innings = st.number_input("Innings", min_value=0, value=record[3])
                runs = st.number_input("Runs", min_value=0, value=record[4])
                average = st.number_input("Average", min_value=0.0, value=float(record[5]), format="%.2f")

                updated = st.form_submit_button("Update")
                if updated:
                    cursor.execute(
                       "UPDATE records SET player_name=%s, matches=%s, innings=%s, runs=%s, average=%s WHERE player_id=%s",
                       (name, matches, innings, runs, average, player_id)
                    )
                    conn.commit()
                    st.success(f"✅ Player {name} updated successfully!")

                    # Refresh the record so form shows new values
                    cursor.execute("SELECT * FROM records WHERE player_id=%s", (player_id,))
                    st.session_state['record'] = cursor.fetchone() 


    # Delete 

    elif crud_option == "Delete":
        st.subheader("Delete Player Record")

        player_id = st.number_input("Enter Player ID to Delete", min_value=1)
        if st.button("Delete"):
            cursor.execute("DELETE FROM records WHERE player_id=%s", (player_id,))
            conn.commit()
            st.success(f" Player ID {player_id} deleted successfully!")

