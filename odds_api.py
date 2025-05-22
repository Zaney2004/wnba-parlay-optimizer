import requests
import streamlit as st

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

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"Failed to fetch odds data: {e}")
        return {}

    player_odds = {}
    for game in data:
        bookmakers = game.get("bookmakers", [])
        for bookmaker in bookmakers:
            markets = bookmaker.get("markets", [])
            for market in markets:
                outcomes = market.get("outcomes", [])
                stat_key = market.get("key", "")
                stat_type = stat_key.split("_")[-1] if "_" in stat_key else stat_key
                for outcome in outcomes:
                    name = outcome.get("name")
                    odds = outcome.get("price")
                    if name:
                        if name not in player_odds:
                            player_odds[name] = {}
                        player_odds[name][stat_type] = odds

    return player_odds
