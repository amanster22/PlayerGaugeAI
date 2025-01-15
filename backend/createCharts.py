import matplotlib.pyplot as plt
import seaborn as sns
from webscrapeData import updateData
import pandas as pd
import plotly.express as px
from scipy.stats import linregress

updateData()

def interactiveBubblePlot(data, player_name=None):
    # Prepare the data
    
    data['SALARY_MILLIONS'] = data['SALARY'] / 1000000  # Salary in millions
    data['SCALED_PTS'] = round(data['NBA_FANTASY_PTS'] / data['SALARY_MILLIONS'].max()*500)
    print(type(data['NBA_FANTASY_PTS_RANK']))
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
    fig = px.scatter(
        data,
        x='NBA_FANTASY_PTS',
        y='SALARY_MILLIONS',
        size='SCALED_PTS',
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
    fig.write_html("interactive_bubble_plot.html")
