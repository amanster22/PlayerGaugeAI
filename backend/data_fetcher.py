import requests
def fetchPlayerData(playerName, sport='NBA'):
    if sport == 'NBA':
        url = f"https://www.nba.com/stats/players/{playerName}"
        response = requests.get(url)
        return response.json()
    elif sport == "NFL":
        pass

fetchPlayerData("trae young", sport='NBA')