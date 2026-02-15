from webscrapeData import updateData
import datetime
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as MSE
from pathlib import Path
import sqlite3


# =========================
# DATE + SEASON
# =========================

year = datetime.datetime.now().year
date = datetime.datetime.now().strftime("%Y-%m-%d")

database_year = str(year - 1) + '-' + str(year)[-2:]
print("Season:", database_year)

updateData(database_year)


# =========================
# PATH SETUP (RELATIVE)
# =========================

BASE_DIR = Path(__file__).resolve().parent
stats_path = BASE_DIR / f"merged_{date}.csv"

df = pd.read_csv(stats_path)
print(f"✅ Loaded {len(df)} player stat rows.")


# =========================
# SCRAPE SALARY DATA
# =========================

salary_url = "https://www.basketball-reference.com/contracts/players.html"

print("📡 Scraping salary data...")
salary_tables = pd.read_html(salary_url)
salary_df = salary_tables[0]

# Flatten MultiIndex header
if isinstance(salary_df.columns, pd.MultiIndex):
    salary_df.columns = salary_df.columns.get_level_values(1)

print("Salary columns detected:", salary_df.columns)

if database_year not in salary_df.columns:
    raise ValueError(f"{database_year} not found in salary table columns.")

salary_df = salary_df[['Player', database_year]].copy()
salary_df.rename(columns={
    'Player': 'PLAYER_NAME',
    database_year: 'SALARY'
}, inplace=True)

salary_df['SALARY'] = (
    salary_df['SALARY']
    .replace('[\$,]', '', regex=True)
)

salary_df['SALARY'] = pd.to_numeric(salary_df['SALARY'], errors='coerce')
salary_df.dropna(subset=['SALARY'], inplace=True)

print(f"✅ {len(salary_df)} salary rows scraped.")


# =========================
# CLEAN PLAYER NAMES
# =========================

def clean_name(name):
    return (
        str(name)
        .replace('.', '')
        .replace(' Jr', '')
        .replace(' III', '')
        .replace(' II', '')
        .strip()
    )

df['PLAYER_NAME'] = df['PLAYER_NAME'].apply(clean_name)
salary_df['PLAYER_NAME'] = salary_df['PLAYER_NAME'].apply(clean_name)


# =========================
# MERGE STATS + SALARY
# =========================

df = df.merge(salary_df, on="PLAYER_NAME", how="left")
df.dropna(subset=['SALARY'], inplace=True)

print(f"✅ {len(df)} players after salary merge.")


# =========================
# FEATURE PREP
# =========================

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

if 'SALARY' in numeric_cols:
    numeric_cols.remove('SALARY')

X = df[numeric_cols]
y = df['SALARY']


# =========================
# TRAIN MODEL
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = xgb.XGBRegressor(
    n_estimators=600,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)
rmse = np.sqrt(MSE(y_test, preds))

print(f"\n🔥 Model RMSE: ${rmse:,.2f}")


# =========================
# GENERATE FULL DATASET PREDICTIONS
# =========================

df['PREDICTED_SALARY'] = model.predict(X)

df['SALARY_PCT_CHANGE'] = (
    (df['PREDICTED_SALARY'] - df['SALARY'])
    / df['SALARY']
)

df['VALUE_SCORE'] = (
    df['PREDICTED_SALARY']
    / df['SALARY']
)


# =========================
# PERFORMANCE VERDICT
# =========================

def verdict(pct):
    if pct > 0.15:
        return "Underpaid"
    elif pct < -0.15:
        return "Overpaid"
    else:
        return "Fair Value"

df['PERFORMANCE_VERDICT'] = df['SALARY_PCT_CHANGE'].apply(verdict)

print("✅ Salary valuation metrics added.")


# =========================
# MERGE PLAYER METADATA
# =========================

players_meta_path = BASE_DIR / "df_players.csv"

if players_meta_path.exists():
    players_meta = pd.read_csv(players_meta_path)

    players_meta['PLAYER_NAME'] = (
        players_meta['first_name'].astype(str) + " " +
        players_meta['last_name'].astype(str)
    ).apply(clean_name)

    df = df.merge(
        players_meta,
        on="PLAYER_NAME",
        how="left",
        suffixes=("", "_meta")
    )

    # Drop duplicated team_id if present
    if "team_id_meta" in df.columns:
        df.drop(columns=["team_id_meta"], inplace=True)

    print("✅ Player metadata merged.")
else:
    print("⚠️ df_players.csv not found. Skipping metadata merge.")


# =========================
# CLEAN DUPLICATE COLUMNS
# =========================

# Normalize column names
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(" ", "_", regex=False)
df.columns = df.columns.str.replace("-", "_", regex=False)
df.columns = df.columns.str.lower()   # <-- THIS FIXES YOUR ISSUE

# Remove duplicates AFTER normalization
df = df.loc[:, ~df.columns.duplicated()]

print("Final columns:", df.columns)
print("✅ Column names cleaned and normalized.")


# =========================
# SAVE CSV
# =========================

final_path = BASE_DIR / f"valuated_{date}.csv"
df.to_csv(final_path, index=False)

print("\n🎉 FULL VALUATION DATASET SAVED")
print(f"📁 {final_path}")
print(f"📊 Final rows: {len(df)}")


# =========================
# SAVE TO SQLITE DATABASE
# =========================
print(df.columns)
db_path = BASE_DIR / f"nba_data_{database_year}.db"

print(f"💾 Saving to SQLite database: {db_path}")

conn = sqlite3.connect(db_path)

df.to_sql(
    "player_table",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("✅ Data successfully written to SQLite database.")
