import requests
import streamlit as st

# API-KEY og URL
API_KEY = "2633576928db43ef810a27612bca7e7d"  # Husk at beskytte din API-nøgle!
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# Funktion til at hente kampdata
def get_match_data(league="PL"):
    url = f"{BASE_URL}/competitions/{league}/matches"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        if "matches" in data and data["matches"]:
            return data["matches"]
        else:
            st.warning("Ingen kampe fundet for denne liga.")
            return []
    else:
        st.error(f"Fejl ved hentning af data: {response.status_code}")
        return []

# Simuler holdform (da API'et ikke nødvendigvis giver disse data)
def get_team_form(team_name):
    return round((hash(team_name) % 10) / 10, 2)  # Genererer et tal mellem 0.0 og 1.0

# Predictability Score-beregning
def predictability_score(home_form, away_form, h2h_win_ratio, home_advantage=0.1):
    form_factor = (home_form + (1 - away_form)) / 2
    predictability = (form_factor * 0.6) + (h2h_win_ratio * 0.3) + (home_advantage * 0.1)
    return round(predictability * 100, 2)

# Streamlit webapp
st.title("⚽ Fodbold Predictability Score Bot")

league = st.selectbox("Vælg liga", ["PL", "BL1", "SA", "PD", "FL1"])  # Premier League, Bundesliga osv.
matches = get_match_data(league)

if matches:
    match_options = [f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" for m in matches]
    selected_match = st.selectbox("Vælg kamp", match_options)

    if st.button("Beregn Score"):
        selected_match_data = next(m for m in matches if f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" == selected_match)

        home_team = selected_match_data["homeTeam"]["name"]
        away_team = selected_match_data["awayTeam"]["name"]

        home_form = get_team_form(home_team)
        away_form = get_team_form(away_team)
        h2h_win_ratio = round(abs(home_form - away_form), 2)  # Simulerer H2H-statistik

        score = predictability_score(home_form, away_form, h2h_win_ratio)

        st.subheader(f"🔢 Predictability Score: {score}%")
        st.write(f"🏠 **{home_team} form**: {home_form}")
        st.write(f"🚀 **{away_team} form**: {away_form}")
        st.write(f"⚖️ **H2H win ratio**: {h2h_win_ratio}")
