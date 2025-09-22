# Cricbuzz's  Player SQL Analytics

# 🏏 Cricbuzz Cricket Dashboard  

An **interactive cricket analytics dashboard** built with **Streamlit**, **MySQL**, and the **Cricbuzz API**.  
This project integrates **real-time cricket data**, **SQL-based analytics**, and **CRUD operations** into a single user-friendly web application.  

---

## 🚀 Features  

### 1. 📊 SQL Analytics  
- Predefined **SQL queries** to analyze cricket data from MySQL.  
- Example queries:  
  - List players representing India.  
  - Show matches from the last 30 days.  
  - Top 10 ODI run scorers.  
  - Match wins per team.  
  - Players count by role.  
  - Series started in 2024.  
- Users can select a query from a dropdown, run it, and view results in a DataFrame.  

---

### 2. 🛠️ CRUD Operations with MySQL  
Perform **Create, Read, Update, Delete** on cricket records.  

- **Create**: Add new player details (ID, name, matches, innings, runs, average).  
- **Read**: View all existing player records.  
- **Update**: Modify a player’s stats by fetching their record via Player ID.  
- **Delete**: Remove a player’s record from the database.  

---

### 3. 📌 Player Stats  
Fetches player statistics in real-time from the **Cricbuzz API**.  

- **Search players** by name.  
- Displays:  
  - Player Info (Name, Country, Teams, Role, DOB, Batting & Bowling Style).  
  - Career Stats Summary.  
  - Batting Stats (by format – Test, ODI, T20I, IPL).  
  - Bowling Stats (by format).  

---

### 4. 🏏 Live Scores Dashboard  
Track **live cricket matches** in real-time.  

- Select an ongoing match from the dropdown.  
- Displays:  
  - Series name.  
  - Venue & City.  
  - Format & Match State.  
  - Current Status.  
  - **Live Score Updates** for both teams.  

---

## ⚙️ Tech Stack  

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Database**: MySQL (via `pymysql`)  
- **Backend API**: [Cricbuzz API (RapidAPI)](https://rapidapi.com/)  
- **Python Libraries**:  
  - `streamlit` – UI rendering.  
  - `pymysql` – MySQL connection.  
  - `pandas` – Data handling.  
  - `requests` – API calls.  
  - `datetime` – Time-based queries.  


---

## 🎯 Project Goals  

- To build an **interactive cricket dashboard** that combines **real-time APIs** with **SQL-based analytics**.  
- To provide a **hands-on learning experience** for working with **Streamlit, MySQL, and API integration**.  
- To demonstrate **CRUD operations** in a real-world cricket data context.  
- To enable **data-driven insights** on cricket matches, players, and series.  
- To offer a **user-friendly interface** for fans, analysts, and developers to explore cricket stats.  

---

## 📝 Conclusion  

The **Cricbuzz Cricket Dashboard** successfully integrates **MySQL database queries**, **API-driven player statistics**, and **live match scores** into a single application.  
It not only serves as a **real-time cricket companion**, but also as a **learning project** for mastering data integration, analytics, and interactive dashboards.  

Future improvements like **data visualization**, **player comparisons**, and **historical data storage** will further enhance its usability for both cricket enthusiasts and developers.  
This project highlights how combining **SQL, APIs, and Streamlit** can create powerful, interactive, and insightful applications.  

---










