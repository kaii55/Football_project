import pandas as pd
import numpy as np

def calculate_avg_defensive_height(df):
    """
    Calculate Average Defensive Height for each team.

    Defensive Height is the average vertical position of defensive actions (tackles, pressures, interceptions).

    Args:
        df (pd.DataFrame): Processed J League events DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with Average Defensive Height for each team.
    """

    # Fill missing values and replace None or NaN with "Complete"
    df['pass.outcome.name'] = df['pass.outcome.name'].fillna("Complete").replace({None: "Complete"})

    df_events = df.copy()

    match_ids = df_events["match_id"].unique()

    home_team = []
    away_team = []

    home_height = []
    away_height = []


    ppda = pd.DataFrame()

    for match_id in match_ids:
        df_match = df_events[df_events["match_id"] == match_id]
        
        
        # Identify home and away teams from the match dataset
        home_team_name = df_match['home_team'].unique()[0]
        away_team_name = df_match['away_team'].unique()[0]
        
        
        team_H = df_match.loc[df_match['team.name'] == home_team_name]
        team_A = df_match.loc[df_match['team.name'] == away_team_name]
        
        team1_defensive_actions_H = pd.concat([
            team_H.loc[team_H['type.name'].isin(['Interception', 'Foul Committed', 'Block'])],
            team_H.loc[team_H['duel.type.name'] == "Tackle"]
        ]).drop_duplicates().reset_index(drop=True)


        team2_defensive_actions_A = pd.concat([
            team_A.loc[team_A['type.name'].isin(['Interception', 'Foul Committed', 'Block'])],
            team_A.loc[team_A['duel.type.name'] == "Tackle"]
        ]).drop_duplicates().reset_index(drop=True)
        
        average_locations_player_home = team1_defensive_actions_H.groupby('player.name').agg({'x':['median'],'y':['mean','count']})
        average_locations_player_home.columns = ['x', 'y', 'count']
        
        average_locations_player_away = team2_defensive_actions_A.groupby('player.name').agg({'x':['median'],'y':['mean','count']})
        average_locations_player_away.columns = ['x', 'y', 'count']
        
        
        home_height.append(average_locations_player_home['x'].mean())
        away_height.append(average_locations_player_away['x'].mean())
        
        
        home_team.append(home_team_name)
        away_team.append(away_team_name)
        
    ppda['home_team'] = home_team
    ppda['away_team'] = away_team

    ppda['home_height'] = home_height
    ppda['away_height'] = away_height

    home_data = ppda[['home_team', 'home_height']].copy()
    home_data.rename(columns = {'home_team': 'Team', 'home_height': 'Def Height'}, inplace = True)

    away_data = ppda[['away_team', 'away_height']].copy()
    away_data.rename(columns = {'away_team': 'Team', 'away_height': 'Def Height'}, inplace = True)

    result = pd.concat([home_data, away_data], ignore_index = True)

    average_def = result.groupby('Team')[['Def Height']].mean().reset_index()

    average_def = average_def.sort_values(by='Def Height', ascending=True)
    average_def['Def Height'] = average_def['Def Height'].round(3)


    return average_def

    
    
