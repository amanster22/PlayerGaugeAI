def updateDashboard(playerData):
    html_template = """
    <html>
    <head>
        <title>{player_name} Stats</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                margin: 20px;
                color: #333;
                background-color: GhostWhite;
            }}
            h1 {{
                text-align: center;
                color: #555;
            }}
            img {{
                display: block;
                margin: 0 auto;
                border-radius: 10px;
            }}
            table {{
                width: 80%;
                margin: 20px auto;
                border-collapse: collapse;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                background-color: #fff;
            }}
            th, td {{
                padding: 10px;
                border: 1px solid #ddd;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
                color: #333;
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
            .stat-box {{
                padding: 10px;
                text-align: center;
                font-weight: bold;
                color: #fff;
            }}
            .legend {{
                margin-top: 30px;
                padding: 10px;
                text-align: center;
                background-color: #fff;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            .legend h2 {{
                margin-bottom: 20px;
            }}
            .legend div {{
                margin-bottom: 10px;
                font-weight: bold;
            }}
            .legend .diamond {{
                background-color: #00b0f0; /* Blue for Diamond */
                color: #fff;
            }}
            .legend .elite {{
                background-color: #8e44ad; /* Purple for Elite */
                color: #fff;
            }}
            .legend .gold {{
                background-color: #f39c12; /* Gold */
                color: #fff;
            }}
            .legend .silver {{
                background-color: #bdc3c7; /* Silver */
                color: #fff;
            }}
            .legend .bronze {{
                background-color: #cd7f32; /* Bronze */
                color: #fff;
            }}
            .graph-button {{
                display: block;
                margin: 30px auto;
                padding: 10px 20px;
                background-color: #12c928;
                color: white;
                text-align: center;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                cursor: pointer;
            }}
            .graph-button:hover {{
                background-color: #007bb0;
            }}
            /* Initially hide the graph container */
            #graph-container {{
                display: none;
                margin-top: 30px;
                text-align: center;
            }}
            .graph-container h2{{
                color: 00FF00; /* Text color */
                font-family: Arial, sans-serif; /* Font set to Arial */
                font-weight: bold; /* Bold text */
                text-align: center; /* Centers text */
            }}
            iframe {{
                width: 60%;
                height: 60%;
                border: none;
            }}
        </style>
        <script>

        
            function toggleGraph() {{
                var graphContainer = document.getElementById("graph-container");
                if (graphContainer.style.display === "none") {{
                    graphContainer.style.display = "block";
                    graphContainer.scrollIntoView && graphContainer.scrollIntoView({{ behavior: "smooth" }});
                }} else {{
                    graphContainer.style.display = "none";
                }}
            }}
        </script>

    </head>
    <body>
        <h1>{player_name} Stats</h1>
        <img src="{image_url}" alt="{player_name}'s Picture" width="200">

        <table>
            <tr>
                <th>Team</th><td>{team}</td>
                <th>Height</th><td>{height}</td>
                <th>Weight</th><td>{weight}</td>
                <th>Country</th><td>{country}</td>
            </tr>
            <tr>
                <th>Age</th><td>{age}</td>
                <th>Birthday</th><td>{birthday}</td>
                <th>Draft</th><td>{draft}</td>
                <th>Experience</th><td>{experience}</td>
            </tr>
        </table>

        <table>
            <tr>
                <th>PPG</th><td class="stat-box" style="background-color: {ppg_color};">{ppg}</td>
                <th>APG</th><td class="stat-box" style="background-color: {apg_color};">{apg}</td>
                <th>RPG</th><td class="stat-box" style="background-color: {rpg_color};">{rpg}</td>
                <th>+/-</th><td class="stat-box" style="background-color: {pm_color};">{pm}</td>
            </tr>
        </table>
        <!-- Legend Section -->
        <div class="legend">
            <h2>Player Tier Legend</h2>
            <div class="diamond">Superstar Tier (Top 1-5%)</div>
            <div class="elite">All-Star Tier (Next 10-15%)</div>
            <div class="gold">Solid Starter Tier (Next 25-30%)</div>
            <div class="silver">Rotation/Bench Tier (Next 25-30%)</div>
            <div class="bronze">Development Tier (Bottom 15-20%)</div>
        </div>
        
        <!-- Graph Button -->
        <button class="graph-button" onclick="toggleGraph()">Show Graph</button>

        <!-- Graph Container (Initially Hidden) -->
        <div id="graph-container">
            <h2>Anticipated Player Rank: {pRank}</h2>
            <iframe src="interactive_bubble_plot.html"></iframe>
            
        </div>

        
    </body>
    </html>

    """

    graph_url = "interactive_bubble_plot.html"

    # Split name into first and last parts
    normalizedName = playerData['NORMALIZED_NAME'].iloc[0]
    first, last = normalizedName.split()
    concatName = last[:5] + first[:2] + "01"
    concatName = concatName.lower()
    name = playerData['PLAYER_NAME'].iloc[0]

    # Grade stats based on ranking or some other method
    gradeStats = ["PTS", "REB", "AST", "PLUS_MINUS"]
    colors = []
    placement = playerData['NBA_FANTASY_PTS_RANK'].iloc[0]
    for stat in gradeStats:
        rank = playerData[stat + "_RANK"].iloc[0]
        print(stat,"rank:",rank)
        ranks = [15,75,250,375]
    


        if rank <= ranks[0]:  # Diamond - Top 5%
            colors.append("00b0f0")
        elif rank <= ranks[1]:  # Elite - Next 15%
            colors.append("purple")
        elif rank <= ranks[2]:  # Gold - Next 25%
            colors.append("#f39c12")
        elif rank <= ranks[3]:  # Silver - Next 30%
            colors.append("silver")
        else:  # Bronze - Bottom 25%
            colors.append("#753600")




    # Populate stats (assuming player_data contains the correct fields)
    html_content = html_template.format(
        player_name=name,
        image_url="https://www.basketball-reference.com/req/202012291/images/headshots/" + concatName + ".jpg",
        team=playerData['TEAM_ABBREVIATION'].iloc[0],
        height="UNK",
        weight="UNK",
        country="UNK",
        age=playerData['AGE'].iloc[0],
        birthday="UNK",
        draft="UNK",
        experience="UNK",
        ppg=round(playerData['PTS'], 1).iloc[0],
        rpg=round(playerData['REB'], 1).iloc[0],
        apg=round(playerData['AST'], 1).iloc[0],
        pm=round(playerData['PLUS_MINUS'].iloc[0]/ playerData['GP'],1).iloc[0],
        ppg_color=colors[0],
        rpg_color=colors[1],
        apg_color=colors[2],
        pm_color=colors[3],
        graph_url=graph_url,
        pRank = round(placement)
        
    )
    # Step 3: Write to an HTML file
    file_path = 'playerDashboard.html'
    with open(file_path, 'w') as file:
        file.write(html_content)

    print("Dashboard updated for player:", name)
    