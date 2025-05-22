import requests

def get_prizepicks_wnba_props(stat_filter=None):
    url = "https://api.prizepicks.com/projections"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    data = response.json()

    players = {}
    for item in data["included"]:
        if item["type"] == "new_player":
            players[item["id"]] = item["attributes"]["name"]

    wnba_props = []
    for entry in data["data"]:
        attributes = entry["attributes"]
        stat = attributes["stat_type"]
        if attributes["league"] == "WNBA" and (stat_filter is None or stat == stat_filter):
            player_id = entry["relationships"]["new_player"]["data"]["id"]
            wnba_props.append({
                "player": players.get(player_id),
                "stat": stat,
                "line": attributes["line_score"]
            })

    return wnba_props