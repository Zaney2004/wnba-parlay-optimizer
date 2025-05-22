import requests
import streamlit as st
import json

def get_odds_from_rapidapi():
    url = "https://odds-api.p.rapidapi.com/v4/sports/basketball_wnba/odds"
    querystring = {
        "regions": "us",
        "markets": "player_points,player_rebounds,player_assists",
        "oddsFormat": "decimal"
    }

    headers = {
        "X-RapidAPI-Key": st.secrets["rapidapi_key"],
        "X-RapidAPI-Host": "odds-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    try:
        data = response.json()
    except ValueError:
        st.error("❌ Failed to parse JSON from RapidAPI.")
        return {}

    # TEMP DEBUG: Display full raw JSON
    st.subheader("🔍 Raw Odds API Response")
    st.code(json.dumps(data, indent=2))  # shows pretty-printed JSON in app

    # Check if API returned error
    if isinstance(data, dict) and "message" in data:
        st.error(f"⚠️ Odds API Error: {data['message']}")
        return {}

    player_odds = {}
    for game in data:
        for bookmaker in game.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                for outcome in market.get("outcomes", []):
                    name = outcome["name"]
                    stat_type = market["key"].split("_")[-1]
                    odds = outcome["price"]

                    if name not in player_odds:
                        player_odds[name] = {}
                    player_odds[name][stat_type] = odds

    return player_odds
