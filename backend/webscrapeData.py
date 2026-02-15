# import requests
# import pandas as pd
# from pathlib import Path
# from tqdm import tqdm
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# import datetime


# date = datetime.datetime.now().strftime("%Y-%m-%d")
# print("Today's date:", date)

# BASE_DIR = Path("../database")
# BASE_DIR.mkdir(parents=True, exist_ok=True)

# HEADERS = {
#     "Accept": "application/json, text/plain, */*",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Connection": "keep-alive",
#     "Host": "stats.nba.com",
#     "Origin": "https://www.nba.com",
#     "Referer": "https://www.nba.com/",
#     "User-Agent": (
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) "
#         "Chrome/120.0.0.0 Safari/537.36"
#     ),
#     "x-nba-stats-origin": "stats",
#     "x-nba-stats-token": "true",
# }

# COLUMNS = [
#     'PLAYER_ID','PLAYER_NAME','NICKNAME','TEAM_ID','TEAM_ABBREVIATION',
#     'AGE','GP','W','L','W_PCT','MIN','FGM','FGA','FG_PCT','FG3M','FG3A',
#     'FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV','STL',
#     'BLK','BLKA','PF','PFD','PTS','PLUS_MINUS','NBA_FANTASY_PTS',
#     'DD2','TD3','WNBA_FANTASY_PTS'
# ]


# # =========================
# # SESSION CREATION
# # =========================

# def create_session():
#     session = requests.Session()
#     session.headers.update(HEADERS)

#     retries = Retry(
#         total=5,
#         backoff_factor=1.5,
#         status_forcelist=[429, 500, 502, 503, 504],
#         allowed_methods=["GET"]
#     )

#     adapter = HTTPAdapter(max_retries=retries)
#     session.mount("https://", adapter)
#     session.mount("http://", adapter)
#     return session


# # =========================
# # MAIN DATA UPDATE FUNCTION
# # =========================

# def updateData(season_id: str):
#     date = datetime.datetime.now().strftime("%Y-%m-%d")
#     print("Today's date:", date)
#     dated_output = BASE_DIR / f"merged_{date}.csv"
#     latest_output = BASE_DIR / "merged.csv"

#     # Skip if today's file already exists
#     if dated_output.exists():
#         print(f"✅ {dated_output.name} already exists. Skipping scrape.")
#         return

#     # Remove old merged.csv if it exists
#     if latest_output.exists():
#         latest_output.unlink()

#     params = {
#         "LeagueID": "00",
#         "Season": season_id,
#         "SeasonType": "Regular Season",
#         "PerMode": "Totals",
#         "MeasureType": "Base",
#         "LastNGames": 0,
#         "Month": 0,
#         "OpponentTeamID": 0,
#         "Period": 0,
#         "PaceAdjust": "N",
#         "PlusMinus": "N",
#         "Rank": "N",
#         "TeamID": 0
#     }

#     print("📡 Fetching NBA player stats...")

#     try:
#         with create_session() as session:
#             response = session.get(
#                 "https://stats.nba.com/stats/leaguedashplayerstats",
#                 params=params,
#                 timeout=20
#             )
#             response.raise_for_status()
#             rows = response.json()["resultSets"][0]["rowSet"]

#     except requests.exceptions.RequestException as e:
#         print("❌ NBA Stats connection failed.")
#         print("Reason:", e)
#         return

#     total_players = len(rows)
#     print(f"✅ {total_players} players identified for season {season_id}")

#     nba_df = pd.DataFrame(
#         tqdm(rows, desc="Processing players", unit="player"),
#         columns=COLUMNS
#     )

#     # =========================
#     # MERGE SALARY DATA
#     # =========================

#     salary_path = BASE_DIR / "salaryData.csv"

#     if not salary_path.exists():
#         print("⚠️ salaryData.csv not found. Skipping salary merge.")
#         merged_df = nba_df
#     else:
#         salary_df = (
#             pd.read_csv(salary_path)
#             .rename(columns={"player_id": "PLAYER_NAME"})
#             [["PLAYER_NAME", "2024-25"]]
#         )

#         merged_df = nba_df.merge(
#             salary_df,
#             on="PLAYER_NAME",
#             how="left"
#         ).rename(columns={"2024-25": "SALARY"})

#     # =========================
#     # SAVE FILES
#     # =========================

#     merged_df.to_csv(latest_output, index=False)
#     merged_df.to_csv(dated_output, index=False)

#     print(f"🎉 Done! {total_players} players saved for {season_id}")
#     print(f"📁 Saved as:")
#     print(f"   - {latest_output}")
#     print(f"   - {dated_output}")


# # =========================
# # RUN SCRIPT
# # =========================

# if __name__ == "__main__":
#     updateData("2025-26")



import pandas as pd
from pathlib import Path
from tqdm import tqdm
import datetime

from nba_api.stats.endpoints import leaguedashplayerstats


# =========================
# CONFIG
# =========================

date = datetime.datetime.now().strftime("%Y-%m-%d")
print("Today's date:", date)

BASE_DIR = Path("../database")
BASE_DIR.mkdir(parents=True, exist_ok=True)

COLUMNS_TO_KEEP = [
    'PLAYER_ID','PLAYER_NAME','TEAM_ID','TEAM_ABBREVIATION',
    'AGE','GP','W','L','W_PCT','MIN','FGM','FGA','FG_PCT','FG3M','FG3A',
    'FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV','STL',
    'BLK','PF','PTS','PLUS_MINUS'
]


# =========================
# MAIN DATA UPDATE FUNCTION
# =========================

def updateData(season_id: str):
    dated_output = BASE_DIR / f"merged_{date}.csv"
    latest_output = BASE_DIR / "merged.csv"

    # Skip if today's file already exists
    if dated_output.exists():
        print(f"✅ {dated_output.name} already exists. Skipping scrape.")
        return

    # Remove old merged.csv
    if latest_output.exists():
        latest_output.unlink()

    print("📡 Fetching NBA player stats via nba_api...")

    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season_id,
            season_type_all_star='Regular Season',
            per_mode_detailed='Totals'
        )

        nba_df = stats.get_data_frames()[0]

    except Exception as e:
        print("❌ NBA API request failed.")
        print("Reason:", e)
        return

    print(f"✅ {len(nba_df)} players retrieved.")

    # =========================
    # PROCESS WITH TQDM
    # =========================

    processed_rows = []

    for _, row in tqdm(nba_df.iterrows(), total=len(nba_df), desc="Processing players"):
        processed_rows.append(row)

    nba_df = pd.DataFrame(processed_rows)

    # Keep only selected columns
    nba_df = nba_df[COLUMNS_TO_KEEP]

    # =========================
    # MERGE SALARY DATA
    # =========================

    salary_path = BASE_DIR / "salaryData.csv"

    if not salary_path.exists():
        print("⚠️ salaryData.csv not found. Skipping salary merge.")
        merged_df = nba_df
    else:
        salary_df = (
            pd.read_csv(salary_path)
            .rename(columns={"player_id": "PLAYER_NAME"})
            [["PLAYER_NAME", "2024-25"]]
        )

        merged_df = nba_df.merge(
            salary_df,
            on="PLAYER_NAME",
            how="left"
        ).rename(columns={"2024-25": "SALARY"})

    # =========================
    # SAVE FILES
    # =========================

    merged_df.to_csv(latest_output, index=False)
    merged_df.to_csv(dated_output, index=False)

    print("\n🎉 Done!")
    print(f"📊 Total players saved: {len(merged_df)}")
    print(f"📁 Files created:")
    print(f"   - {latest_output}")
    print(f"   - {dated_output}")


# =========================
# RUN SCRIPT
# =========================

if __name__ == "__main__":
    updateData("2025-26")
