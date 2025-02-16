import requests
import requests
import streamlit as st

# API-KEY og URL
API_KEY = "2633576928db43ef810a27612bca7e7d"
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# Funktion til at hente kampdata
def get_match_data(league="PL"):
    url = f"{BASE_URL}/competitions/{league}/matches"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Fejl ved hentning af data: {response.status_code}")
        return None

# Predictability Score-beregning
def predictability_score(home_form, away_form, h2h_win_ratio, home_advantage=0.1):
    form_factor = (home_form + (1 - away_form)) / 2
    predictability = (form_factor * 0.6) + (h2h_win_ratio * 0.3) + (home_advantage * 0.1)
    return round(predictability * 100, 2)

# Streamlit webapp
st.title("Fodbold Predictability Score Bot")
league = st.selectbox("Vælg liga", ["PL", "BL1", "SA", "PD", "FL1"])  # Premier League, Bundesliga osv.
data = get_match_data(league)

if data:
    matches = data.get("matches", [])
    match_options = [f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" for m in matches]
    selected_match = st.selectbox("Vælg kamp", match_options)
    
    if st.button("Beregn Score"):
        home_form, away_form, h2h_win_ratio = 0.8, 0.5, 0.7  # Midlertidige værdier
        score = predictability_score(home_form, away_form, h2h_win_ratio)
        st.write(f"Predictability Score: {score}%")
import streamlit as st

# API-KEY og URL
API_KEY = "2633576928db43ef810a27612bca7e7d"
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# Funktion til at hente kampdata
def get_match_data(league="PL"):
    url = f"{BASE_URL}/competitions/{league}/matches"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Fejl ved hentning af data: {response.status_code}")
        return None

# Predictability Score-beregning
def predictability_score(home_form, away_form, h2h_win_ratio, home_advantage=0.1):
    form_factor = (home_form + (1 - away_form)) / 2
    predictability = (form_factor * 0.6) + (h2h_win_ratio * 0.3) + (home_advantage * 0.1)
    return round(predictability * 100, 2)

# Streamlit webapp
st.title("Fodbold Predictability Score Bot")
league = st.selectbox("Vælg liga", ["PL", "BL1", "SA", "PD", "FL1"])  # Premier League, Bundesliga osv.
data = get_match_data(league)

if data:
    matches = data.get("matches", [])
    match_options = [f"{m['homeTeam']['name']} vs {m['awayTeam']['name']}" for m in matches]
    selected_match = st.selectbox("Vælg kamp", match_options)
    
    if st.button("Beregn Score"):
        home_form, away_form, h2h_win_ratio = 0.8, 0.5, 0.7  # Midlertidige værdier
        score = predictability_score(home_form, away_form, h2h_win_ratio)
        st.write(f"Predictability Score: {score}%")
