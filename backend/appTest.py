import pandas as pd
import numpy as np
import webbrowser
import unicodedata
from updateDashboard import updateDashboard
from webscrapeData import updateData
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

from createCharts import interactiveBubblePlot
from fuzzywuzzy import process

from createCharts import interactiveBubblePlot, gen_ppg_plot, gen_apg_plot, gen_rpg_plot, gen_fan_plot




updateData('2024-25')
data = pd.read_csv('../database/merged.csv')
player_dict = dict(zip(data['PLAYER_NAME'], data['PLAYER_ID']))

# Function to find the closest matching player
def get_player_id(user_input):
    best_match, score = process.extractOne(user_input, player_dict.keys())
    
    if score > 80:  # Set a threshold for similarity
        return player_dict[best_match]  # Return the corresponding ID
    else:
        return "No close match found."
def normalize_text(text):
    normalized_text = unicodedata.normalize('NFD', text)  # Decompose characters
    normalized_text = ''.join([c for c in normalized_text if not unicodedata.combining(c)])  # Remove accents
    return normalized_text.lower()

# Get data from csv file and create updated dataframe: converting each stat to per game stat

gen_ppg_plot()
gen_apg_plot()
gen_rpg_plot()
gen_fan_plot
data = pd.read_csv('../database/merged.csv')


data.rename(columns={'2024-25': 'SALARY'}, inplace=True)

data['PLAYER_NAME'] = data['PLAYER_NAME'].astype(str)
data['PTS'] = data['PTS'] / data['GP']
data['AST'] = data['AST'] / data['GP']
data['REB'] = data['REB'] / data['GP']
data['MIN'] = data['MIN'] / data['GP']
data['FGA'] = data['FGA'] / data['GP']
data['FGM'] = data['FGM'] / data['GP']
data['PLUS_MINUS'] = data['PLUS_MINUS'] / data['GP']
data['NORMALIZED_NAME'] = data['PLAYER_NAME'].apply(normalize_text)
data['NBA_FANTASY_PTS'] = data['NBA_FANTASY_PTS'] / data['GP']
data = data.dropna(subset=['SALARY'])
data['SALARY'] = data['SALARY'].replace('[\$,]', '', regex=True).str.strip()
data['SALARY'] = pd.to_numeric(data['SALARY'], errors='coerce')

selected_features = ['GP', 'AGE', 'PTS', 'AST', 'REB', 'MIN', 'PLUS_MINUS', 'FGM','FGA','W_PCT']
selected_features = ['MIN', 'FGM', 'FGA', 'FTM', 'FTA', 'AST','TOV','PFD', 'PTS','NBA_FANTASY_PTS']
X = data[selected_features]
y = data['SALARY']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



# Standardizing Features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Training the Random Forest Regressor Model
rf_model = RandomForestRegressor(max_depth=None, min_samples_split=10, n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)


# Salary Prediction Function
def predict_salary_rf(model, scaler, stats):
    """
    Predict the salary of a player based on their stats.
    Args:
        model: Trained regression model.
        scaler: StandardScaler used for scaling features.
        stats: List of player stats in the same order as selected_features.
    Returns:
        Predicted salary as a float.
    """
    stats_scaled = scaler.transform([stats])  # Scale the input stats
    predicted_salary = model.predict(stats_scaled)  # Predict salary
    return predicted_salary[0]

# Get specified player data via User Input and Evaluate performance via contract
nameInput=input("What NBA player would you like to analyze first?: ")
name_id = get_player_id(nameInput)


playerData = data[data['PLAYER_ID'] == name_id]
playerName = playerData['PLAYER_NAME'].iloc[0]


stats_columns = selected_features[:]
stats_columns.append('SALARY')

feature_importances = rf_model.feature_importances_

importance_df = pd.DataFrame({
    'Feature': selected_features,
    'Importance': feature_importances
})

importance_df = importance_df.sort_values(by='Importance', ascending=False)
print(importance_df)
if playerData.empty:
    print("Player not found in the dataset.")
else:
    playerStats = playerData[stats_columns[:-1]].iloc[0].tolist()
    playerSalary = playerData[stats_columns].iloc[0, -1] # extract last column of row
    predicted_salary = predict_salary_rf(rf_model, scaler, playerStats)
    playerData['PREDICTED_SALARY'] = predicted_salary
    print(f"The predicted salary for {playerName} is: ${predicted_salary:,.2f}")

    if predicted_salary - playerSalary > 1500000:
        print(f"{playerName} is exceeding expectations for his current contract")

    elif (abs(predicted_salary - playerSalary) < 1500000):
        print(predicted_salary - playerSalary)
        print(f"{playerName} is playing at level with his contract")
    else:
        print(f"{playerName} is playing at a level below his contract value")
        
    print(f"The actual salary for {playerName} is: ${playerSalary:,.2f}")

interactiveBubblePlot(data, playerName)
updateDashboard(playerData)


