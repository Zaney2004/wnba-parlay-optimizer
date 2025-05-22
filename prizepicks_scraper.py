import requests

def get_prizepicks_wnba_props(stat_filter=None):
    url = "https://api.prizepicks.com/projections"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching PrizePicks data: {e}")
        return []

    players = {}
    for item in data.get("included", []):
        if item.get("type") == "new_player":
            players[item["id"]] = item["attributes"]["name"]

    wnba_props = []
    for entry in data.get("data", []):
        attributes = entry.get("attributes", {})
        stat = attributes.get("stat_type")
        if attributes.get("league") == "WNBA" and (stat_filter is None or stat == stat_filter):
            player_id = entry.get("relationships", {}).get("new_player", {}).get("data", {}).get("id")
            if player_id and player_id in players:
                wnba_props.append({
                    "player": players[player_id],
                    "stat": stat,
                    "line": attributes.get("line_score")
                })

    return wnba_props
