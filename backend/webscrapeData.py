# import requests
# import pandas as pd
# from datetime import datetime

# def updateData(season_id):
#     per_mode = 'Totals'

#     player_info_url='https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode='+per_mode+'&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season='+season_id+'&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
#     headers  = {
#         'Connection': 'keep-alive',
#         'Accept': 'application/json, text/plain, */*',
#         'x-nba-stats-token': 'true',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
#         'x-nba-stats-origin': 'stats',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-Mode': 'cors',
#         'Referer': 'https://stats.nba.com/',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'en-US,en;q=0.9',
#     }

#     response = requests.get(url=player_info_url,headers=headers).json()
#     player_info = response['resultSets'][0]['rowSet']

#     headers= ['PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'NBA_FANTASY_PTS', 'DD2', 'TD3', 'WNBA_FANTASY_PTS', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 'NBA_FANTASY_PTS_RANK', 'DD2_RANK', 'TD3_RANK', 'WNBA_FANTASY_PTS_RANK']
#     nba_df_p = pd.DataFrame(player_info,columns=headers)
#     nba_df_p.to_excel('../database/UPDATED.xlsx')

#     salaryData = pd.read_csv('../database/salaryData.csv')
#     salaryData = salaryData.rename(columns={'player_id': 'PLAYER_NAME'})

#     merged_df = nba_df_p.merge(salaryData[['PLAYER_NAME', '2024-25']], on="PLAYER_NAME", how="left")
#     merged_df = merged_df.rename(columns={season_id:'SALARY'})

#     merged_df.to_excel('../database/merged.xlsx')
#     merged_df.to_csv('../database/merged.csv',index=False)
#     merged_df.to_csv('/Users/amanshaik/Documents/GitHub/PlayerGaugeAI/database/merged.csv',index=False)
#     print('updated Data in ../database/merged.csv')
#     print(season_id)
import requests
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_DIR = Path("../database")

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "stats.nba.com",
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
}

COLUMNS = [
    'PLAYER_ID','PLAYER_NAME','NICKNAME','TEAM_ID','TEAM_ABBREVIATION',
    'AGE','GP','W','L','W_PCT','MIN','FGM','FGA','FG_PCT','FG3M','FG3A',
    'FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV','STL',
    'BLK','BLKA','PF','PFD','PTS','PLUS_MINUS','NBA_FANTASY_PTS',
    'DD2','TD3','WNBA_FANTASY_PTS'
]

def create_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    retries = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def updateData(season_id: str):
    params = {
        "LeagueID": "00",
        "Season": season_id,
        "SeasonType": "Regular Season",
        "PerMode": "Totals",
        "MeasureType": "Base",
        "LastNGames": 0,
        "Month": 0,
        "OpponentTeamID": 0,
        "Period": 0,
        "PaceAdjust": "N",
        "PlusMinus": "N",
        "Rank": "N",
        "TeamID": 0
    }

    print("📡 Fetching NBA player stats...")

    try:
        with create_session() as session:
            response = session.get(
                "https://stats.nba.com/stats/leaguedashplayerstats",
                params=params,
                timeout=20
            )
            response.raise_for_status()
            rows = response.json()["resultSets"][0]["rowSet"]

    except requests.exceptions.RequestException as e:
        print("❌ NBA Stats connection failed.")
        print("Reason:", e)
        return

    total_players = len(rows)
    print(f"✅ {total_players} players identified for season {season_id}")

    nba_df = pd.DataFrame(
        tqdm(rows, desc="Processing players", unit="player"),
        columns=COLUMNS
    )

    salary_df = (
        pd.read_csv(BASE_DIR / "salaryData.csv")
        .rename(columns={"player_id": "PLAYER_NAME"})
        [["PLAYER_NAME", "2024-25"]]
    )

    merged_df = nba_df.merge(
        salary_df,
        on="PLAYER_NAME",
        how="left"
    ).rename(columns={"2024-25": "SALARY"})

    merged_df.to_csv(BASE_DIR / "merged.csv", index=False)
    merged_df.to_csv(
        "/Users/amanshaik/Documents/GitHub/PlayerGaugeAI/database/merged.csv",
        index=False
    )

    print(f"🎉 Done! {total_players} players saved for {season_id}")
