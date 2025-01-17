from flask import Flask, request, render_template
import pandas as pd
import unicodedata
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__,template_folder='frontend/templates')

# Load and preprocess the data
data = pd.read_csv('database/merged.csv')
data.rename(columns={'2024-25': 'SALARY'}, inplace=True)
data['PLAYER_NAME'] = data['PLAYER_NAME'].astype(str)
data['PTS'] = data['PTS'] / data['GP']
data['AST'] = data['AST'] / data['GP']
data['REB'] = data['REB'] / data['GP']
data['MIN'] = data['MIN'] / data['GP']
data['FGA'] = data['FGA'] / data['GP']
data['FGM'] = data['FGM'] / data['GP']
data['PLUS_MINUS'] = data['PLUS_MINUS'] / data['GP']
data['NORMALIZED_NAME'] = data['PLAYER_NAME'].apply(lambda x: unicodedata.normalize('NFD', x).encode('ascii', 'ignore').decode('utf-8').lower())
data['NBA_FANTASY_PTS'] = data['NBA_FANTASY_PTS'] / data['GP']
data['SALARY'] = pd.to_numeric(data['SALARY'].replace('[\$,]', '', regex=True).str.strip(), errors='coerce')
data = data.dropna(subset=['SALARY'])

selected_features = ['GP', 'AGE', 'PTS', 'AST', 'REB', 'NBA_FANTASY_PTS', 'MIN', 'PLUS_MINUS', 'FGM','FGA','W_PCT']
X = data[selected_features]
y = data['SALARY']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

rf_model = RandomForestRegressor(max_depth=None, min_samples_split=10, n_estimators=100, random_state=42)
rf_model.fit(X_scaled, y)

# Normalize text function
def normalize_text(text):
    normalized_text = unicodedata.normalize('NFD', text)
    return ''.join([c for c in normalized_text if not unicodedata.combining(c)]).lower()

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

@app.route('/predict', methods=['POST'])
def predict():
    player_name = request.form['playerName']  # Retrieve player name from form
    print(f"Player name received: {player_name}")
    normalized_name = normalize_text(player_name)
    player_data = data[data['NORMALIZED_NAME'] == normalized_name]
    # print('searching name')
    
    if player_data.empty:
        return f"Player '{player_name}' not found in the dataset."
    
    player_stats = player_data[selected_features].iloc[0].tolist()
    player_salary = player_data['SALARY'].iloc[0]
    predicted_salary = rf_model.predict(scaler.transform([player_stats]))[0]
    
    return (f"The predicted salary for {player_name} is: ${predicted_salary:,.2f}<br>"
            f"The actual salary is: ${player_salary:,.2f}<br>"
            f"{'Exceeding' if predicted_salary - player_salary > 1_500_000 else 'Meeting'} expectations!")

if __name__ == '__main__':
    app.run(debug=True)
