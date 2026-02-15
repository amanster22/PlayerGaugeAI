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

BASE_DIR = Path(__file__).resolve().parent
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
