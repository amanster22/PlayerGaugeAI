import matplotlib.pyplot as plt
import seaborn as sns
# from webscrapeData import updateData
import pandas as pd
import plotly.express as px
from scipy.stats import linregress
import plotly.graph_objects as go
# updateData()

def interactiveBubblePlot(data, player_name=None):
    # Prepare the data
    data['SCALED_AGE'] = (data['AGE'] - data['AGE'].min()) / (data['AGE'].max() - data['AGE'].min()) * 40 + 5
    data['MARKER_SIZE'] = 5
    data['SALARY_MILLIONS'] = data['SALARY'] / 1000000  # Salary in millions
    data['SCALED_PTS'] = round(data['NBA_FANTASY_PTS'] / data['SALARY_MILLIONS'].max()*500)
    # data['NBA_FANTASY_PTS_RANK'] = int(data['NBA_FANTASY_PTS_RANK'])
    # Highlight a player if provided
    if player_name:
        name = player_name
        player_name = player_name.lower()
        data['HIGHLIGHT'] = data['PLAYER_NAME'].str.lower() == player_name

        # Create a new column to store the color for each player
        data['PLAYER'] = data['HIGHLIGHT'].map({True: name, False: 'Other'})
    else:
        # If no player is highlighted, default to blue or another color
        data['PLAYER'] = 'blue'  # Change to 'blue' or any other fallback color
    # Create the interactive bubble plot
    radius = 10
    fig = px.scatter(
        data,
        x='NBA_FANTASY_PTS',
        y='SALARY_MILLIONS',
        size='SCALED_AGE',
        color='PLAYER', 
        hover_name='PLAYER_NAME',
        hover_data={
            'NBA_FANTASY_PTS_RANK': ':.2f',
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
        legend=dict(
        x=1,  # x position (1 is fully to the right side of the plot)
        y=1,  # y position (1 is the top of the plot)
        xanchor='left',  # Anchor the legend's left side to the x position
        yanchor='top',  # Anchor the legend's top side to the y position
        orientation='v',  # Set legend orientation to vertical ('h' for horizontal)
        font=dict(size=12),  # Font size of the legend labels
        bgcolor='rgba(0,0,0,0.1)',  # Semi-transparent background for readability
        bordercolor='black',  # Border color for the legend box
        borderwidth=2,  # Border width for the legend box
    ),
        margin=dict(l=40, r=30, t=40, b=40),  # Add extra margin on the right for the legend
        autosize=True,

    )


    # Save the interactive plot as an HTML file
    fig.write_html("../frontend/templates/interactive_bubble_plot.html")
    fig.write_html("interactive_bubble_plot.html")





def gen_ppg_plot():
    # Calculate Points Per Game (PPG)
    data = pd.read_csv('../database/merged.csv')
    data.rename(columns={'2024-25': 'SALARY'}, inplace=True)
    data['SALARY'] = data['SALARY'].replace('[\$,]', '', regex=True).str.strip()
    data['SALARY'] = pd.to_numeric(data['SALARY'], errors='coerce')

    data['PPG'] = data['PTS'] / data['GP']
    ppgSalary = data[['PLAYER_NAME', 'PPG', 'SALARY']].sort_values(by='PPG', ascending=False).reset_index()

    # Get top 5 players
    top5 = ppgSalary.head(5)


    # Create bar chart with heatmap-based coloring on salary
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top5['PLAYER_NAME'],
        y=top5['PPG'],
        marker=dict(color=top5['SALARY'], colorscale='Blues', colorbar=dict(title='SALARY')),
        name='PPG'
    ))

    # Update layout
    fig.update_layout(
        title='Top 5 Players by PPG',
        xaxis_title='Player',
        yaxis_title='Points Per Game',
        coloraxis=dict(colorbar=dict(title='SALARY')),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )

    # Save figure to HTML
    fig.write_html("../frontend/templates/top5_players_ppg.html")
    fig.write_html("top5_players_ppg.html")

def gen_apg_plot():
    # Calculate Points Per Game (PPG)
    data = pd.read_csv('../database/merged.csv')
    data.rename(columns={'2024-25': 'SALARY'}, inplace=True)
    data['SALARY'] = data['SALARY'].replace('[\$,]', '', regex=True).str.strip()
    data['SALARY'] = pd.to_numeric(data['SALARY'], errors='coerce')

    data['APG'] = data['AST'] / data['GP']
    apgSalary = data[['PLAYER_NAME', 'APG', 'SALARY']].sort_values(by='APG', ascending=False).reset_index()

    # Get top 5 players
    top5 = apgSalary.head(5)


    # Create bar chart with heatmap-based coloring on salary
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top5['PLAYER_NAME'],
        y=top5['APG'],
        marker=dict(color=top5['SALARY'], colorscale='Oranges', colorbar=dict(title='SALARY')),
        name='APG'
    ))

    # Update layout
    fig.update_layout(
        title='Top 5 Players by APG',
        xaxis_title='Player',
        yaxis_title='Assists Per Game',
        coloraxis=dict(colorbar=dict(title='SALARY')),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )

    # Save figure to HTML
    fig.write_html("../frontend/templates/top5_players_apg.html")
    fig.write_html("top5_players_apg.html")

def gen_rpg_plot():
    # Calculate Points Per Game (PPG)
    data = pd.read_csv('../database/merged.csv')
    data.rename(columns={'2024-25': 'SALARY'}, inplace=True)
    data['SALARY'] = data['SALARY'].replace('[\$,]', '', regex=True).str.strip()
    data['SALARY'] = pd.to_numeric(data['SALARY'], errors='coerce')

    data['RPG'] = data['REB'] / data['GP']
    rpgSalary = data[['PLAYER_NAME', 'RPG', 'SALARY']].sort_values(by='RPG', ascending=False).reset_index()

    # Get top 5 players
    top5 = rpgSalary.head(5)


    # Create bar chart with heatmap-based coloring on salary
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top5['PLAYER_NAME'],
        y=top5['RPG'],
        marker=dict(color=top5['SALARY'], colorscale='Greens', colorbar=dict(title='SALARY')),
        name='RPG'
    ))

    # Update layout
    fig.update_layout(
        title='Top 5 Players by RPG',
        xaxis_title='Player',
        yaxis_title='Rebounds Per Game',
        coloraxis=dict(colorbar=dict(title='SALARY')),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )

    # Save figure to HTML
    fig.write_html("../frontend/templates/top5_players_rpg.html")
    fig.write_html("top5_players_rpg.html")

def gen_fan_plot():
    # Calculate Points Per Game (PPG)
    data = pd.read_csv('../database/merged.csv')
    data.rename(columns={'2024-25': 'SALARY'}, inplace=True)
    data['SALARY'] = data['SALARY'].replace('[\$,]', '', regex=True).str.strip()
    data['SALARY'] = pd.to_numeric(data['SALARY'], errors='coerce')

    data['FPG'] = data['NBA_FANTASY_PTS'] / data['GP']
    fpgSalary = data[['PLAYER_NAME', 'FPG', 'SALARY']].sort_values(by='FPG', ascending=False).reset_index()

    # Get top 5 players
    top5 = fpgSalary.head(5)


    # Create bar chart with heatmap-based coloring on salary
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top5['PLAYER_NAME'],
        y=top5['FPG'],
        marker=dict(color=top5['SALARY'], colorscale='Purples', colorbar=dict(title='SALARY')),
        name='FPG'
    ))

    # Update layout
    fig.update_layout(
        title='Top 5 Players by FPG',
        xaxis_title='Player',
        yaxis_title='Fantast Points Per Game',
        coloraxis=dict(colorbar=dict(title='SALARY')),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )

    # Save figure to HTML
    fig.write_html("../frontend/templates/top5_players_fpg.html")
    fig.write_html("top5_players_fpg.html")
