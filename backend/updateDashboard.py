def updateDashboard(playerData):
    html_template = """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{player_name} Stats</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 text-gray-900">

        <!-- Header -->
    <header class="bg-blue-600 text-white shadow-lg">
        <div class="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
            <!-- Logo and Title -->
            <div class="flex items-center space-x-4">
                <img src="https://via.placeholder.com/50" alt="Logo" class="w-10 h-10 rounded-full">
                <h1 class="text-2xl font-bold">PlayerGaugeAI</h1>
            </div>
            <!-- Navigation Links -->
            <nav>
                <ul class="flex space-x-6">
                    <li><a href="#" class="hover:text-blue-200">Home</a></li>
                    <li><a href="#" class="hover:text-blue-200">Players</a></li>
                    <li><a href="#" class="hover:text-blue-200">About</a></li>
                    <li><a href="#" class="hover:text-blue-200">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
        

            <!-- Leaders Sections -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <div class="bg-white p-4 rounded-lg shadow-md">
                    <h3 class="text-xl font-semibold text-center">PG Leaders</h3>
                    <div id="pg-leaders-graph" class="mt-4">
                        <iframe src="{ppg_graph_url}" class="w-full h-96 border-none"></iframe>
                    </div>
                </div>
                <div class="bg-white p-4 rounded-lg shadow-md">
                    <h3 class="text-xl font-semibold text-center">AST Leaders</h3>
                    <div id="ast-leaders-graph" class="mt-4">
                        <iframe src="{apg_graph_url}" class="w-full h-96 border-none"></iframe>
                    </div>
                </div>
                <div class="bg-white p-4 rounded-lg shadow-md">
                    <h3 class="text-xl font-semibold text-center">REB Leaders</h3>
                    <div id="reb-leaders-graph" class="mt-4">
                        <iframe src="{rpg_graph_url}" class="w-full h-96 border-none"></iframe>
                    </div>
                </div>
                <div class="bg-white p-4 rounded-lg shadow-md">
                    <h3 class="text-xl font-semibold text-center">Fantasy Points Leaders</h3>
                    <div id="salary-leaders-graph" class="mt-4">
                        <iframe src="{fpg_graph_url}" class="w-full h-96 border-none"></iframe>
                    </div>
                </div>
            </div>
            <div class="max-w-4xl mx-auto p-6">
            <!-- Search Bar and Button -->
        <div class="flex justify-center items-center space-x-4">
            <input
                type="text"
                id="playerName"
                placeholder="Enter player name"
                class="w-64 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
                id="searchButton"
                class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
                Search
            </button>
        </div>
            <!-- Player Search Section -->
            <div class="bg-white p-6 rounded-lg shadow-md mb-8">
                <h2 class="text-2xl font-semibold text-center mb-6">Player Search</h2>
                <div class="flex flex-col items-center">
                    <img src="{image_url}" alt="{player_name}'s Picture" class="rounded-lg shadow-md w-48">
                    <h3 class="text-xl font-semibold text-blue-600 mt-4">Anticipated Player Rank: {pRank}</h3>
                    <h3 class="text-xl font-semibold text-green-600">24-25 Season Salary: {salary}</h3>
                    <h3 class="text-xl font-semibold text-red-600">Predicted Salary: {predSalary}</h3>
                </div>

                <div class="mt-6">
                    <table class="w-full border-collapse bg-white shadow-md rounded-lg overflow-hidden">
                        <tbody>
                            <tr class="bg-gray-100">
                                <th class="px-4 py-2 border">Team</th><td class="px-4 py-2 border">{team}</td>
                                <th class="px-4 py-2 border">Height</th><td class="px-4 py-2 border">{height}</td>
                                <th class="px-4 py-2 border">Weight</th><td class="px-4 py-2 border">{weight}</td>
                                <th class="px-4 py-2 border">Country</th><td class="px-4 py-2 border">{country}</td>
                            </tr>
                            <tr>
                                <th class="px-4 py-2 border">Age</th><td class="px-4 py-2 border">{age}</td>
                                <th class="px-4 py-2 border">Birthday</th><td class="px-4 py-2 border">{birthday}</td>
                                <th class="px-4 py-2 border">Draft</th><td class="px-4 py-2 border">{draft}</td>
                                <th class="px-4 py-2 border">Experience</th><td class="px-4 py-2 border">{experience}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="mt-6">
                    <table class="w-full border-collapse bg-white shadow-md rounded-lg overflow-hidden">
                        <tbody>
                            <tr class="text-center">
                                <th class="px-4 py-2 border">PPG</th><td class="px-4 py-2 border text-white font-bold" style="background-color: {ppg_color};">{ppg}</td>
                                <th class="px-4 py-2 border">APG</th><td class="px-4 py-2 border text-white font-bold" style="background-color: {apg_color};">{apg}</td>
                                <th class="px-4 py-2 border">RPG</th><td class="px-4 py-2 border text-white font-bold" style="background-color: {rpg_color};">{rpg}</td>
                                <th class="px-4 py-2 border">+/-</th><td class="px-4 py-2 border text-white font-bold" style="background-color: {pm_color};">{pm}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Player Tier Legend -->
            <div class="mt-8 bg-white p-6 rounded-lg shadow-md">
                <h2 class="text-2xl font-semibold text-center">Player Tier Legend</h2>
                <div class="mt-4 space-y-2 text-center">
                    <div class="bg-blue-500 text-white py-2 rounded-lg">Superstar Tier (Top 1-5%)</div>
                    <div class="bg-purple-500 text-white py-2 rounded-lg">All-Star Tier (Next 10-15%)</div>
                    <div class="bg-yellow-500 text-white py-2 rounded-lg">Solid Starter Tier (Next 25-30%)</div>
                    <div class="bg-gray-400 text-white py-2 rounded-lg">Rotation/Bench Tier (Next 25-30%)</div>
                    <div class="bg-orange-600 text-white py-2 rounded-lg">Development Tier (Bottom 15-20%)</div>
                </div>
            </div>

            <!-- Graph Toggle Button -->
            <div class="text-center mt-6">
                <button onclick="toggleGraph()" class="px-6 py-3 bg-green-500 text-white rounded-lg shadow hover:bg-green-700">Show Graph</button>
            </div>

            <!-- Graph Container -->
            <div id="graph-container" class="hidden mt-6 text-center">
                <iframe src="{graph_url}" class="w-full h-96 border-none"></iframe>
            </div>
        </div>

        <script>
            function toggleGraph() {{
                var graphContainer = document.getElementById("graph-container");
                graphContainer.classList.toggle("hidden");
                if (!graphContainer.classList.contains("hidden")) {{
                    graphContainer.scrollIntoView({{ behavior: "smooth" }});
                }}
            }}
        </script>
    </body>
    </html>
    """
    ppg_graph_url = "top5_players_ppg.html"
    apg_graph_url = "top5_players_apg.html"
    rpg_graph_url = "top5_players_rpg.html"
    fpg_graph_url = "top5_players_fpg.html"
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
        ppg_graph_url = ppg_graph_url,
        apg_graph_url = apg_graph_url,
        rpg_graph_url = rpg_graph_url,
        fpg_graph_url = fpg_graph_url,
        pRank = round(placement),
        salary = playerData['SALARY'].iloc[0],
        predSalary = playerData['PREDICTED_SALARY'].iloc[0]
        
    )
    # Step 3: Write to an HTML file
    file_path = 'playerDashboard.html'
    with open(file_path, 'w') as file:
        file.write(html_content)

    print("Dashboard updated for player:", name)
    