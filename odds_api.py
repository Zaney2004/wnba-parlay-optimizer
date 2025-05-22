import requests

def get_odds_from_official_api(api_key):
    url = "https://api.the-odds-api.com/v4/sports/basketball_wnba/odds"
    params = {
        "regions": "us",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "decimal",
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # For now, just return all data or parse it as needed
    return data
