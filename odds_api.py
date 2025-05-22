import requests
import streamlit as st
import json

def get_odds_from_rapidapi():
    url = "https://livesportsodds.p.rapidapi.com/odds"
    querystring = {
        "sport": "basketball_wnba",
        "region": "us"
    }

    headers = {
        "X-RapidAPI-Key": st.secrets["rapidapi_key"],
        "X-RapidAPI-Host": "livesportsodds.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    try:
        data = response.json()
    except ValueError:
        st.error("❌ Failed to parse JSON from RapidAPI.")
        return {}

    # DEBUG: show full API response
    st.subheader("🔍 Raw Odds API Response")
    st.code(json.dumps(data, indent=2))

    # You must inspect what 'data' contains to parse it correctly
    # This is a placeholder structure
    player_odds = {}

    # Replace the below parsing with actual structure once visible
    for game in data.get("games", []):
        for market in game.get("markets", []):
            for outcome in market.get("outcomes", []):
                name = outcome.get("name")
                stat_type = market.get("key", "").split("_")[-1]
                odds = outcome.get("price")

                if name not in player_odds:
                    player_odds[name] = {}
                player_odds[name][stat_type] = odds

    return player_odds
