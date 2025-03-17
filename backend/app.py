from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import unicodedata
from updateDashboard import updateDashboard
from webscrapeData import updateData
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from createCharts import interactiveBubblePlot, gen_ppg_plot, gen_apg_plot, gen_rpg_plot, gen_fan_plot

app = Flask(__name__, template_folder='../frontend/templates')

# Update and preprocess data
updateData('2024-25')
gen_ppg_plot()
gen_apg_plot()
gen_rpg_plot()
gen_fan_plot()

def normalize_text(text):
    normalized_text = unicodedata.normalize('NFD', text)
    normalized_text = ''.join([c for c in normalized_text if not unicodedata.combining(c)])
    return normalized_text.lower()

# Load dataset
data = pd.read_csv('../database/merged.csv')
data.rename(columns={'2024-25': 'SALARY'}, inplace=True)
data['PLAYER_NAME'] = data['PLAYER_NAME'].astype(str)
for stat in ['PTS', 'AST', 'REB', 'MIN', 'FGA', 'FGM', 'PLUS_MINUS', 'NBA_FANTASY_PTS']:
    data[stat] = data[stat] / data['GP']
data['NORMALIZED_NAME'] = data['PLAYER_NAME'].apply(normalize_text)
data['SALARY'] = pd.to_numeric(data['SALARY'].replace('[\$,]', '', regex=True), errors='coerce')
data = data.dropna(subset=['SALARY'])

# Define features and train model
selected_features = ['GP', 'AGE', 'PTS', 'AST', 'REB', 'NBA_FANTASY_PTS', 'MIN', 'PLUS_MINUS', 'FGM', 'FGA', 'W_PCT']
X = data[selected_features]
y = data['SALARY']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
rf_model = RandomForestRegressor(max_depth=None, min_samples_split=10, n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

def predict_salary_rf(model, scaler, stats):
    stats_scaled = scaler.transform([stats])
    return model.predict(stats_scaled)[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    player_name = request.form['player_name']
    normalized_name = normalize_text(player_name)
    player_data = data[data['NORMALIZED_NAME'] == normalized_name]
    if player_data.empty:
        return jsonify({'error': 'Player not found'})
    player_stats = player_data[selected_features].iloc[0].tolist()
    predicted_salary = predict_salary_rf(rf_model, scaler, player_stats)
    player_data['PREDICTED_SALARY'] = predicted_salary
    return jsonify({'player': player_name, 'predicted_salary': f"${predicted_salary:,.2f}"})

@app.route('/dashboard/<player_name>')
def dashboard(player_name):
    normalized_name = normalize_text(player_name)
    player_data = data[data['NORMALIZED_NAME'] == normalized_name]
    if player_data.empty:
        return 'Player not found', 404
    html_content = updateDashboard(player_data)
    return html_content

if __name__ == '__main__':
    app.run(debug=True)