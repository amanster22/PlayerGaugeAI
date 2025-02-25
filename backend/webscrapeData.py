import requests
import pandas as pd
from datetime import datetime

# current_datetime = datetime.now()
# month = current_datetime.month

# if month > 10:
#     currentSeason = current_datetime.year
# else:
#     currentSeason = current_datetime.year - 1

# startYr = str(currentSeason)
# endYr = str(currentSeason+1)[-2:]
# season_id = startYr + '-' + endYr

# def updateData():
#     current_datetime = datetime.now()
#     month = current_datetime.month

#     if month > 10:
#         currentSeason = current_datetime.year
#     else:
#         currentSeason = current_datetime.year - 1

#     startYr = str(currentSeason)
#     endYr = str(currentSeason+1)[-2:]
#     season_id = startYr + '-' + endYr
#     per_mode = 'Totals'

#     player_info_url='https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode='+per_mode+'&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season='+season_id+'&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
#     headers  = {
#         'Connection': 'keep-alive',
#         'Accept': 'application/json, text/plain, */*',
#         'x-nba-stats-token': 'true',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
#         'x-nba-stats-origin': 'stats',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-Mode': 'cors',
#         'Referer': 'https://stats.nba.com/',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'en-US,en;q=0.9',
#     }

#     response = requests.get(url=player_info_url,headers=headers).json()
#     player_info = response['resultSets'][0]['rowSet']

#     # headers_list = response['resultSets'][0]['headers']
#     # print("Column headers from the API response:")
#     # print('headers:',headers_list)

#     headers= ['PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'NBA_FANTASY_PTS', 'DD2', 'TD3', 'WNBA_FANTASY_PTS', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 'NBA_FANTASY_PTS_RANK', 'DD2_RANK', 'TD3_RANK', 'WNBA_FANTASY_PTS_RANK']
#     nba_df_p = pd.DataFrame(player_info,columns=headers)
#     nba_df_p.to_excel('../database/UPDATED.xlsx')

#     # salaryData = pd.read_excel('../database/salaryData.xlsx')
#     salaryData = pd.read_csv('../database/salaryData.csv')
#     salaryData = salaryData.rename(columns={'player_id': 'PLAYER_NAME'})

#     merged_df = nba_df_p.merge(salaryData[['PLAYER_NAME', '2024-25']], on="PLAYER_NAME", how="left")

#     # Save the merged DataFrame to CSV without index
#     merged_df.to_excel('../database/merged.xlsx')
#     merged_df.to_csv('../database/merged.csv',index=False)

def updateData(season_id):
    # current_datetime = datetime.now()
    # month = current_datetime.month

    # if month > 10:
    #     currentSeason = current_datetime.year
    # else:
    #     currentSeason = current_datetime.year - 1

    # startYr = str(currentSeason)
    # endYr = str(currentSeason+1)[-2:]
    # season_id = startYr + '-' + endYr
    per_mode = 'Totals'

    player_info_url='https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode='+per_mode+'&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season='+season_id+'&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
    headers  = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-nba-stats-token': 'true',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'x-nba-stats-origin': 'stats',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://stats.nba.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get(url=player_info_url,headers=headers).json()
    player_info = response['resultSets'][0]['rowSet']

    # headers_list = response['resultSets'][0]['headers']
    # print("Column headers from the API response:")
    # print('headers:',headers_list)

    headers= ['PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'NBA_FANTASY_PTS', 'DD2', 'TD3', 'WNBA_FANTASY_PTS', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 'NBA_FANTASY_PTS_RANK', 'DD2_RANK', 'TD3_RANK', 'WNBA_FANTASY_PTS_RANK']
    nba_df_p = pd.DataFrame(player_info,columns=headers)
    nba_df_p.to_excel('../database/UPDATED.xlsx')

    # salaryData = pd.read_excel('../database/salaryData.xlsx')
    salaryData = pd.read_csv('../database/salaryData.csv')
    salaryData = salaryData.rename(columns={'player_id': 'PLAYER_NAME'})

    merged_df = nba_df_p.merge(salaryData[['PLAYER_NAME', '2024-25']], on="PLAYER_NAME", how="left")

    # Save the merged DataFrame to CSV without index
    merged_df.to_excel('../database/merged.xlsx')
    merged_df.to_csv('../database/merged.csv',index=False)
    print('updated Data')
