import matplotlib.pyplot as plt
import seaborn as sns
from webscrapeData import updateData
import pandas as pd
import plotly.express as px


updateData()

def interactiveBubblePlot(data, player_name=None):
    # Prepare the data
    data['SCALED_PTS'] = data['NBA_FANTASY_PTS'] / data['NBA_FANTASY_PTS'].max() * 350
    data['SALARY_MILLIONS'] = data['SALARY'] / 1000000  # Salary in millions

    # Highlight a player if provided
    if player_name:
        name = player_name
        player_name = player_name.lower()
        print(player_name)
        data['HIGHLIGHT'] = data['PLAYER_NAME'].str.lower() == player_name

        # Create a new column to store the color for each player
        data['PLAYER'] = data['HIGHLIGHT'].map({True: name, False: 'Other'})
    else:
        # If no player is highlighted, default to blue or another color
        data['PLAYER'] = 'blue'  # Change to 'blue' or any other fallback color
    # Create the interactive bubble plot
    fig = px.scatter(
        data,
        x='NBA_FANTASY_PTS',
        y='SALARY_MILLIONS',
        size='SCALED_PTS',
        color='PLAYER', 
        hover_name='PLAYER_NAME',
        hover_data={
            'NBA_FANTASY_PTS': ':.2f',
            'SALARY_MILLIONS': ':.2f',
            'AGE': True,
            'PTS': ':.2f',
        },
        title="NBA Salary vs Fantasy Points with Age and Points",
    )

    # Update the traces with custom line styling (optional)
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    
    # Update the layout with labels
    fig.update_layout(
        xaxis_title="NBA Fantasy Points",
        yaxis_title="Salary (in $ millions)",
        legend_title="Player Status",
        template="plotly_dark",
    )

    # Save the interactive plot as an HTML file
    fig.write_html("interactive_bubble_plot.html")
