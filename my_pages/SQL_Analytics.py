import streamlit as st
import pandas as pd
from db import connect_pymysql

def run():
    st.title("📊 Cricket SQL Analytics")

    sql_questions = {

        #beginner
        "1. Selecting players who represent India": """
             SELECT p.player_id,
             p.full_name,p.role,
             p.batting_style,p.bowling_style
            FROM players_info p
            WHERE LOWER(p.country) = 'india'
            ORDER BY p.full_name;
        """,
        "2. Show all cricket matches that were played in the last 30 days": """
            SELECT
            m.match_id,
            m.match_desc AS match_description,
            m.team1,m.team2,
            v.venue_name AS venue,v.city,
            m.start_date
            FROM matches_info m
            LEFT JOIN venues v ON v.venue_id = v.venue_id
            WHERE m.start_date BETWEEN (CURRENT_DATE - INTERVAL '30' DAY) AND CURRENT_DATE
            ORDER BY m.start_date DESC;
        """,
        "3.Top 10 ODI run scorers with runs, average" :"""
        SELECT player_name, runs,average
FROM top_odi_runs
ORDER BY runs DESC
LIMIT 10;

 """,




        "4.Venues with capacity > 50,000" : """
        SELECT
  venue_id,
  venue_name,
  city,
  country,
  capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
 """,



        "5.Count matches won by each team." :"""SELECT match_winner AS team_name, 
COUNT(*) AS total_wins
FROM end_to_end_match_info
GROUP BY team_name
ORDER BY total_wins DESC;
 """,



        "6.Count players by playing role." :"""SELECT
  role,
  COUNT(*) AS player_count
FROM players_info
GROUP BY role
ORDER BY player_count DESC; """,




        "7.Highest individual score in Test, ODI, T20I formats." :"""
        SELECT 
e.format AS match_format, MAX(b.runs) AS highest_score
FROM batsmen_data b
JOIN end_to_end_match_info e ON b.match_id = e.match_id
GROUP BY match_format;
 """,




        "8.Series started in 2024 with name, host, type, start date, matches.":"""
        SELECT
  series_name,
  venue,
  format,
  match_date
FROM end_to_end_match_info
WHERE EXTRACT(YEAR FROM match_date) = 2024
ORDER BY match_date;
 """,



        #intermediate
        "9.All-rounders with >1000 runs & >50 wickets." :"""
        SELECT 
full_name AS player_name, 
total_runs AS runs_scored, 
total_wickets AS wickets_taken
FROM players_info
WHERE role LIKE '%Allrounder%'
AND total_runs > 1000
AND total_wickets > 50;
 """,




        "10.Last 20 matches with teams, winner, margin, venue." :"""
        SELECT match_desc AS match_description,
                   team1 AS team_one,
                   team2 AS team_two,
                   SUBSTRING_INDEX(status, ' won by ', 1) AS winning_team,
                   SUBSTRING_INDEX(SUBSTRING_INDEX(status, ' won by ', -1), ' ', 1) AS victory_margin,
                   CASE
                       WHEN status LIKE '%won by%run%' THEN 'Runs'
                       WHEN status LIKE '%won by%wkt%' THEN 'Wickets'
                       ELSE NULL
                   END AS victory_type,
                   venue AS venue_name
            FROM matches_recent_1
            WHERE state = 'Complete'
            ORDER BY STR_TO_DATE(start_date, '%d-%m-%Y %H:%i') DESC
            LIMIT 20;

 """,




        "11.Compare players’ runs & averages across formats." :"""
        SELECT player_name, test_runs, odi_runs, t20_runs,
                   ROUND(
                        (test_runs + odi_runs + t20_runs) / 
                        (
                            (CASE WHEN test_runs > 0 THEN 1 ELSE 0 END) + 
                            (CASE WHEN odi_runs > 0 THEN 1 ELSE 0 END) + 
                            (CASE WHEN t20_runs > 0 THEN 1 ELSE 0 END)
                        ), 
                   2) AS overall_batting_average
            FROM player_stats
            WHERE 
                (CASE WHEN test_runs > 0 THEN 1 ELSE 0 END) + 
                (CASE WHEN odi_runs > 0 THEN 1 ELSE 0 END) + 
                (CASE WHEN t20_runs > 0 THEN 1 ELSE 0 END) >= 2
            ORDER BY overall_batting_average DESC; """,





    
        "12:Team wins at home vs away." :"""
        SELECT team_stats.team AS team_name,
                   team_stats.home_or_away,
                   COUNT(*) AS total_wins
            FROM (
                SELECT team1 AS team,
                       CASE 
                           WHEN status LIKE CONCAT(team1, ' won%') AND series_name LIKE CONCAT('%tour of ', team1, '%') THEN 'Home'
                           WHEN status LIKE CONCAT(team1, ' won%') THEN 'Away'
                       END AS home_or_away
                FROM matches_with_scores
                WHERE status LIKE '%won%'
                UNION ALL
                SELECT team2 AS team,
                       CASE 
                           WHEN status LIKE CONCAT(team2, ' won%') AND series_name LIKE CONCAT('%tour of ', team2, '%') THEN 'Home'
                           WHEN status LIKE CONCAT(team2, ' won%') THEN 'Away'
                       END AS home_or_away
                FROM matches_with_scores
                WHERE status LIKE '%won%'
            ) AS team_stats
            WHERE home_or_away IS NOT NULL
            GROUP BY team_stats.team, team_stats.home_or_away
            ORDER BY team_stats.team, team_stats.home_or_away;
 """,




        "13.Partnerships (consecutive batsmen) scoring ≥100 runs." :"""
        SELECT p1.match_id, p1.innings_no, p1.batter1_name AS batter1, p1.batter2_name AS batter2,
                   p1.runs_partnership + p2.runs_partnership AS combined_runs
            FROM partnerships_data p1
            JOIN partnerships_data p2
                ON p1.match_id = p2.match_id
               AND p1.innings_no = p2.innings_no
               AND p1.wicket_fallen + 1 = p2.wicket_fallen
            WHERE (p1.runs_partnership + p2.runs_partnership) >= 100
            ORDER BY p1.match_id, p1.innings_no, p1.wicket_fallen;
             """,




        "14.Bowlers’ venue stats: economy, wickets, matches." :"""
        SELECT player_name, venue, COUNT(DISTINCT match_id) AS matches_played,
                   SUM(wickets) AS total_wickets,
                   ROUND(AVG(economy_rate), 2) AS avg_economy_rate
            FROM bowling
            WHERE overs >= 4
            GROUP BY player_name, venue
            HAVING COUNT(DISTINCT match_id) >= 2
            ORDER BY player_name, venue; """,





        "15.Players’ performance in close matches (<50 runs or <5 wkts)." :"""
        SELECT p.player_id, p.full_name AS player_name,
                   AVG(b.runs) AS avg_runs,
                   COUNT(DISTINCT b.match_id) AS close_matches_played,
                   SUM(CASE WHEN c.match_winner = b.team THEN 1 ELSE 0 END) AS matches_won
            FROM batsmen_data b
            JOIN end_to_end_match_info c ON b.match_id = c.match_id
            JOIN players_info p ON b.player_id = p.player_id
            WHERE (
                    (c.win_margin LIKE '%runs' AND CAST(SUBSTRING_INDEX(c.win_margin, ' ', 1) AS UNSIGNED) < 50)
                 OR (c.win_margin LIKE '%wkt%' AND CAST(SUBSTRING_INDEX(c.win_margin, ' ', 1) AS UNSIGNED) < 5)
                  )
            GROUP BY p.player_id, p.full_name
            ORDER BY close_matches_played DESC; """,




        "16.Yearly batting avg & strike rate since 2020 (min 5 matches)." :"""
        SELECT
  LOWER(m.toss_decision) AS toss_decision,
  COUNT(*) AS total_matches_with_decision,
  SUM(CASE WHEN m.toss_winner = m.match_winner THEN 1 ELSE 0 END) AS toss_winner_wins,
  ROUND(100.0 * SUM(CASE WHEN m.toss_winner = m.match_winner THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0), 2) AS pct_wins_by_toss_winner
FROM end_to_end_match_info m
WHERE m.toss_decision IS NOT NULL
GROUP BY LOWER(m.toss_decision)
ORDER BY pct_wins_by_toss_winner DESC; """,




        #advanced

        "17.Toss effect: % wins when winning toss (bat/bowl choice)." :"""SELECT
  LOWER(m.toss_decision) AS toss_decision,
  COUNT(*) AS total_matches_with_decision,
  SUM(CASE WHEN m.toss_winner = m.match_winner THEN 1 ELSE 0 END) AS toss_winner_wins,
  ROUND(100.0 * SUM(CASE WHEN m.toss_winner = m.match_winner THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0), 2) AS pct_wins_by_toss_winner
FROM end_to_end_match_info m
WHERE m.toss_decision IS NOT NULL
GROUP BY LOWER(m.toss_decision)
ORDER BY pct_wins_by_toss_winner DESC; """,



        "18.Economical bowlers in ODIs/T20s (≥10 matches, ≥2 overs avg)." :"""
        WITH bowler_agg AS (
SELECT player_id, player_name, COUNT(DISTINCT match_id) AS matches_played,
SUM(overs) AS total_overs, SUM(runs_conceded) AS total_runs, SUM(wickets) AS total_wickets,
SUM(overs) * 1.0 / COUNT(DISTINCT match_id) AS avg_overs_per_match,
SUM(runs_conceded) * 1.0 / SUM(overs) AS economy_rate
FROM bowling
GROUP BY player_id, player_name
HAVING COUNT(DISTINCT match_id) >= 2 AND SUM(overs) * 1.0 / COUNT(DISTINCT match_id) >= 1
),
ranked_bowlers AS (
SELECT *, RANK() OVER (ORDER BY total_wickets DESC, economy_rate ASC) AS bowler_rank
FROM bowler_agg
)
SELECT bowler_rank AS ranking, player_name, matches_played, total_overs, total_runs, total_wickets,
ROUND(economy_rate, 2) AS economy_rate
FROM ranked_bowlers
ORDER BY bowler_rank;

 """,


        "19.Consistent batsmen: avg & std dev of runs (since 2022)." :"""
        WITH player_innings AS (
SELECT player_id, player_name, match_id, runs, balls_faced
FROM batting
WHERE match_date >= '1970-01-01' AND balls_faced >= 10
),
player_stats AS (
SELECT player_id, player_name, COUNT(DISTINCT match_id) AS innings_played,
AVG(runs) AS avg_runs, STDDEV(runs) AS run_stddev
FROM player_innings
GROUP BY player_id, player_name
HAVING COUNT(DISTINCT match_id) >= 2
)
SELECT player_name, innings_played, ROUND(avg_runs, 2) AS avg_runs,
ROUND(run_stddev, 2) AS run_stddev
FROM player_stats
ORDER BY run_stddev ASC, avg_runs DESC; """,




        "20.Matches played & batting avg in Tests/ODIs/T20s (≥20 total)." :"""
        WITH player_format_stats AS (
                SELECT b.player_id, b.player_name, c.format,
                COUNT(DISTINCT b.match_id) AS matches_played,
                SUM(b.runs) AS total_runs,
                SUM(CASE WHEN b.dismissal <> 'not out' THEN 1 ELSE 0 END) AS outs
                FROM batsmen_data b
                JOIN end_to_end_match_info c ON b.match_id = c.match_id
                GROUP BY b.player_id, b.player_name, c.format
             ),
player_summary AS (
SELECT player_id, player_name,
SUM(CASE WHEN format = 'TEST' THEN matches_played ELSE 0 END) AS test_matches,
SUM(CASE WHEN format = 'ODI'  THEN matches_played ELSE 0 END) AS odi_matches,
SUM(CASE WHEN format = 'T20'  THEN matches_played ELSE 0 END) AS t20_matches,
ROUND(SUM(CASE WHEN format = 'TEST' THEN total_runs ELSE 0 END) * 1.0 /
	NULLIF(SUM(CASE WHEN format = 'TEST' THEN outs ELSE 0 END), 0), 2) AS test_bat_avg,
ROUND(SUM(CASE WHEN format = 'ODI' THEN total_runs ELSE 0 END) * 1.0 /
	NULLIF(SUM(CASE WHEN format = 'ODI' THEN outs ELSE 0 END), 0), 2) AS odi_bat_avg,
ROUND(SUM(CASE WHEN format = 'T20' THEN total_runs ELSE 0 END) * 1.0 /
	NULLIF(SUM(CASE WHEN format = 'T20' THEN outs ELSE 0 END), 0), 2) AS t20_bat_avg
FROM player_format_stats
GROUP BY player_id, player_name
)
SELECT *
FROM player_summary
WHERE (test_matches + odi_matches + t20_matches) >= 10
ORDER BY (test_matches + odi_matches + t20_matches) DESC;
 """,




        "21.Rank players using weighted batting, bowling, fielding score." :"""
        WITH batting_stats AS (
                SELECT 
                    player_id,
                    MIN(player_name) AS player_name,
                    c.format,
                    SUM(runs) AS runs_scored,
                    ROUND(SUM(runs) / NULLIF(SUM(CASE WHEN dismissal <> 'not out' THEN 1 END),0), 2) AS batting_avg,
                    ROUND(AVG(strike_rate), 2) AS strike_rate
                FROM batsmen_data b
                JOIN end_to_end_match_info c ON b.match_id = c.match_id
                GROUP BY player_id, c.format
            ),
            bowling_stats AS (
                SELECT
                    player_id,
                    MIN(player_name) AS player_name,
                    c.format,
                    SUM(wickets) AS wickets_taken,
                    ROUND(SUM(runs_conceded) / NULLIF(SUM(wickets), 0), 2) AS bowling_avg,
                    ROUND(SUM(runs_conceded) / NULLIF(SUM(overs), 0), 2) AS economy_rate
                FROM bowlers_data bo
                JOIN end_to_end_match_info c ON bo.match_id = c.match_id
                GROUP BY player_id, c.format
            ),
            fielding_stats AS (
                SELECT
                    player_id,
                    c.format,
                    SUM(catches) AS catches,
                    SUM(stumpings) AS stumpings
                FROM fielding f
                JOIN end_to_end_match_info c ON f.match_id = c.match_id
                GROUP BY player_id, c.format
            ),
            combined AS (
                SELECT  
                    b.player_id,
                    b.player_name,
                    b.format,
                    b.runs_scored,
                    b.batting_avg,
                    b.strike_rate,
                    IFNULL(bo.wickets_taken,0) AS wickets_taken,
                    IFNULL(bo.bowling_avg,50) AS bowling_avg,
                    IFNULL(bo.economy_rate,6) AS economy_rate,
                    IFNULL(f.catches,0) AS catches,
                    IFNULL(f.stumpings,0) AS stumpings
                FROM batting_stats b
                LEFT JOIN bowling_stats bo ON b.player_id = bo.player_id AND b.format = bo.format
                LEFT JOIN fielding_stats f ON b.player_id = f.player_id AND b.format = f.format
            ),
            scored AS (
                SELECT
                    player_id,
                    player_name,
                    format,
                    (runs_scored * 0.01 + batting_avg * 0.5 + strike_rate * 0.3) AS batting_points,
                    (wickets_taken * 2 + (50 - bowling_avg) * 0.5 + (6 - economy_rate) * 2) AS bowling_points,
                    (catches * 1 + stumpings * 2) AS fielding_points
                FROM combined
            ),
            ranked AS (
                SELECT
                    player_id,
                    player_name,
                    format,
                    ROUND(batting_points + bowling_points + fielding_points, 2) AS total_score,
                    RANK() OVER (PARTITION BY format ORDER BY (batting_points + bowling_points + fielding_points) DESC) AS rank_in_format
                FROM scored
            )
            SELECT *
            FROM ranked
            WHERE rank_in_format <= 20
            ORDER BY format, rank_in_format; """,




        "22.Head-to-head team stats (≥5 matches in last 3 yrs)." :""" 
        WITH recent_matches AS (
                SELECT *
                FROM end_to_end_match_info
                WHERE match_date >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
            ),
            team_pairs AS (
                SELECT 
                    LEAST(team1, team2) AS team_a,
                    GREATEST(team1, team2) AS team_b,
                    COUNT(*) AS matches_played
                FROM recent_matches
                GROUP BY LEAST(team1, team2), GREATEST(team1, team2)
                HAVING matches_played >= 3
            ),
            match_details AS (
                SELECT 
                    m.match_id,
                    LEAST(m.team1, m.team2) AS team_a,
                    GREATEST(m.team1, m.team2) AS team_b,
                    m.team1,
                    m.team2,
                    m.match_winner,
                    m.win_margin,
                    m.toss_winner,
                    m.toss_decision,
                    m.venue,
                    m.format
                FROM recent_matches m
                JOIN team_pairs tp 
                    ON LEAST(m.team1, m.team2) = tp.team_a 
                AND GREATEST(m.team1, m.team2) = tp.team_b
            ),
            team_stats AS (
                SELECT
                    team_a,
                    team_b,
                    SUM(CASE WHEN match_winner = team_a THEN 1 ELSE 0 END) AS wins_team_a,
                    SUM(CASE WHEN match_winner = team_b THEN 1 ELSE 0 END) AS wins_team_b,
                    ROUND(AVG(CASE WHEN match_winner = team_a THEN win_margin END), 2) AS avg_margin_team_a,
                    ROUND(AVG(CASE WHEN match_winner = team_b THEN win_margin END), 2) AS avg_margin_team_b
                FROM match_details
                GROUP BY team_a, team_b
            ),
            venue_performance AS (
                SELECT
                    LEAST(team1, team2) AS team_a,
                    GREATEST(team1, team2) AS team_b,
                    venue,
                    toss_decision,
                    SUM(CASE WHEN match_winner = team1 THEN 1 ELSE 0 END) AS wins_team1,
                    SUM(CASE WHEN match_winner = team2 THEN 1 ELSE 0 END) AS wins_team2,
                    COUNT(*) AS total_matches
                FROM recent_matches
                GROUP BY LEAST(team1, team2), GREATEST(team1, team2), venue, toss_decision
            ),
            overall_win_pct AS (
                SELECT
                    team_a,
                    team_b,
                    ROUND(100 * wins_team_a / NULLIF((wins_team_a + wins_team_b),0), 2) AS win_pct_team_a,
                    ROUND(100 * wins_team_b / NULLIF((wins_team_a + wins_team_b),0), 2) AS win_pct_team_b
                FROM team_stats
            )
            SELECT 
                ts.team_a,
                ts.team_b,
                (ts.wins_team_a + ts.wins_team_b) AS total_matches,
                ts.wins_team_a,
                ts.wins_team_b,
                ts.avg_margin_team_a,
                ts.avg_margin_team_b,
                ow.win_pct_team_a,
                ow.win_pct_team_b
            FROM team_stats ts
            JOIN overall_win_pct ow ON ts.team_a = ow.team_a AND ts.team_b = ow.team_b
            ORDER BY total_matches DESC, ts.team_a, ts.team_b; """,





        "23.Player form from last 10 innings: avg, strike rate, 50s, consistency." :"""
            WITH player_last10 AS (
                SELECT
                    player_id,
                    player_name,
                    runs,
                    strike_rate,
                    ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY match_date DESC) AS rn
                FROM batting
            ),
            recent_matches AS (
                SELECT *
                FROM player_last10
                WHERE rn <= 10
            ),
            metrics AS (
                SELECT
                    player_id,
                    player_name,
                    ROUND(AVG(CASE WHEN rn <= 5 THEN runs END), 2) AS last5_avg,
                    ROUND(AVG(runs), 2) AS last10_avg,
                    ROUND(AVG(strike_rate), 2) AS avg_strike_rate,
                    SUM(CASE WHEN runs >= 50 THEN 1 ELSE 0 END) AS scores_50plus,
                    ROUND(STDDEV(runs), 2) AS consistency
                FROM recent_matches
                GROUP BY player_id, player_name
            ),
            player_form AS (
                SELECT *,
                    CASE
                        WHEN last5_avg >= 100 THEN 'Excellent Form'
                        WHEN last5_avg >= 60 THEN 'Good Form'
                        WHEN last5_avg >= 30 THEN 'Average Form'
                        ELSE 'Poor Form'
                    END AS form_category
                FROM metrics
            )
            SELECT *
            FROM player_form
            ORDER BY last5_avg DESC;
 """,



        "24.Best partnerships (≥5 innings together): avg, 50+ count, highest, success %." :""" 
        
        WITH partnership_stats AS (
                SELECT
                    batter1_name,
                    batter2_name,
                    COUNT(*) AS total_partnerships,
                    ROUND(AVG(runs_partnership), 2) AS avg_runs,
                    SUM(CASE WHEN runs_partnership > 50 THEN 1 ELSE 0 END) AS partnerships_over_50,
                    MAX(runs_partnership) AS highest_partnership,
                    ROUND(
                        CASE 
                            WHEN COUNT(*) = 0 THEN 0
                            ELSE SUM(CASE WHEN runs_partnership > 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
                        END, 2
                    ) AS success_rate
                FROM partnerships_data
                GROUP BY batter1_name, batter2_name
                HAVING COUNT(*) >= 1
            ),
            ranked_partnerships AS (
                SELECT *,
                    ROW_NUMBER() OVER (ORDER BY success_rate DESC, avg_runs DESC, highest_partnership DESC) AS `ranking`
                FROM partnership_stats
            )
            SELECT *
            FROM ranked_partnerships
            WHERE `ranking` <= 20;
             """,



        "25.Time-series: quarterly batting trends, career phase (rising/declining/stable)." :""" 
    
            WITH player_match_order AS (
                SELECT 
                    player_id,
                    player_name,
                    match_id,
                    runs,
                    strike_rate,
                    ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY match_id) AS match_order
                FROM batting
            ),
            player_quarters AS (
                SELECT
                    player_id,
                    player_name,
                    CEIL(match_order / 3) AS quarter_number,  -- every 3 matches = 1 quarter
                    COUNT(match_id) AS matches_played,
                    AVG(runs) AS avg_runs,
                    AVG(strike_rate) AS avg_sr
                FROM player_match_order
                GROUP BY player_id, player_name, CEIL(match_order / 3)
                HAVING COUNT(match_id) >= 3
            ),
            player_with_trend AS (
                SELECT
                    player_id,
                    player_name,
                    CONCAT('Q', quarter_number) AS year_quarter,
                    avg_runs,
                    avg_sr,
                    LAG(avg_runs) OVER (PARTITION BY player_id ORDER BY quarter_number) AS prev_avg_runs,
                    LAG(avg_sr) OVER (PARTITION BY player_id ORDER BY quarter_number) AS prev_avg_sr
                FROM player_quarters
            ),
            player_trend_analysis AS (
                SELECT
                    player_id,
                    player_name,
                    year_quarter,
                    avg_runs,
                    avg_sr,
                    CASE
                        WHEN prev_avg_runs IS NULL THEN 'N/A'
                        WHEN avg_runs > prev_avg_runs AND avg_sr > prev_avg_sr THEN 'Improving'
                        WHEN avg_runs < prev_avg_runs AND avg_sr < prev_avg_sr THEN 'Declining'
                        ELSE 'Stable'
                    END AS performance_trend
                FROM player_with_trend
            )
            SELECT 
                player_id,
                player_name,
                COUNT(CASE WHEN performance_trend = 'Improving' THEN 1 END) AS improving_quarters,
                COUNT(CASE WHEN performance_trend = 'Declining' THEN 1 END) AS declining_quarters,
                COUNT(CASE WHEN performance_trend = 'Stable' THEN 1 END) AS stable_quarters,
                CASE
                    WHEN COUNT(CASE WHEN performance_trend = 'Improving' THEN 1 END) >
                        COUNT(CASE WHEN performance_trend = 'Declining' THEN 1 END)
                    THEN 'Career Ascending'
                    WHEN COUNT(CASE WHEN performance_trend = 'Declining' THEN 1 END) >
                        COUNT(CASE WHEN performance_trend = 'Improving' THEN 1 END)
                    THEN 'Career Declining'
                    ELSE 'Career Stable'
                END AS career_phase
            FROM player_trend_analysis
        GROUP BY player_id, player_name;
        """
}

    selected_query = st.selectbox("Select a query:", list(sql_questions.keys()))
    query_to_run = sql_questions[selected_query]

    if st.button("Run Query"):
        conn = connect_pymysql()
        df = pd.read_sql(query_to_run, conn)
        st.dataframe(df)
        conn.close()
