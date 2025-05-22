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

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    player_odds = {}
    for game in data:
        for bookmaker in game.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                for outcome in market.get("outcomes", []):
                    name = outcome["name"]
                    stat_type = market["key"].split("_")[-1]  # e.g., 'points', 'rebounds'
                    odds = outcome["price"]

                    if name not in player_odds:
                        player_odds[name] = {}
                    player_odds[name][stat_type] = odds

    return player_odds
