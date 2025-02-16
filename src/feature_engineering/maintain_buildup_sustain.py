import pandas as pd
import numpy as np

def calculate_maintain_buildup_sustain(df):
    """
    Calculate Maintain buildup and Sustain Percentages.

    Maintain measures how often teams retain possession after passing sequences.

    Args:
        df (pd.DataFrame): Processed J League events DataFrame.

    Returns:
        pd.DataFrame: DataFrame with Maintain percentage.
    """

    df_events = df.copy()

    match_ids = df_events["match_id"].unique()

    home_team = []
    away_team = []

    home_maintain = []
    away_maintain = []

    home_build = []
    away_build = []

    home_sustain = []
    away_sustain = []

    week = []
    match = []

    for match_id in match_ids:
        df_match = df_events[df_events["match_id"] == match_id]
        
        df_match['Time'] = df_match['minute'] * 60 + df_match['second']
        df_match['Time_diff'] = df_match['Time'].diff()
        df_match['Time_diff'].fillna(0, inplace = True)
        df_match["Time_diff"] = df_match["Time_diff"].shift(-1)
        
        df_match = df_match.loc[df_match['type.name'].isin(['Pass'])]
        
        
        # Identify home and away teams from the match dataset
        home_team_name = df_match['home_team'].unique()[0]
        away_team_name = df_match['away_team'].unique()[0]
        
        # Create copies for possession calculation
        pos_A = df_match[df_match['possession_team.name'] == home_team_name]
        pos_B = df_match[df_match['possession_team.name'] == away_team_name]
        
        
        """---------------------------------"""
        
        def is_maintain(x, pass_end_x):
            if (x < 60.0) and (pass_end_x < 60.0):
                return True  
            else:
                return False
            
        def is_buildup(x, pass_end_x):
            if (x > 60.0) and (pass_end_x < 102):
                return True  
            else:
                return False
            
        def is_sustain(x, pass_end_x):
            if (x > 90.0) and (pass_end_x > 90.0):
                return True  
            else:
                return False
                
        
        """---------------------------------"""
        
        pos_A["is_maintain"] = pos_A.apply(lambda row : is_maintain(row['x'], row['pass_end_x']), axis = 1)

        pos_B["is_maintain"] = pos_B.apply(lambda row : is_maintain(row['x'], row['pass_end_x']), axis = 1)
        
        pos_A["is_buildup"] = pos_A.apply(lambda row : is_buildup(row['x'], row['pass_end_x']), axis = 1)

        pos_B["is_buildup"] = pos_B.apply(lambda row : is_buildup(row['x'], row['pass_end_x']), axis = 1)
        
        
        pos_A["is_sustain"] = pos_A.apply(lambda row : is_sustain(row['x'], row['pass_end_x']), axis = 1)
        
        pos_B["is_sustain"] = pos_B.apply(lambda row : is_sustain(row['x'], row['pass_end_x']), axis = 1)
        
        """---------------------------------"""
    
        team_A_maintain = pos_A.loc[pos_A['is_maintain'] == True]
        team_B_maintain = pos_B.loc[pos_B['is_maintain'] == True]
        
        team_A_buildup = pos_A.loc[pos_A['is_buildup'] == True]
        team_B_buildup = pos_B.loc[pos_B['is_buildup'] == True]
        
        team_A_sustain = pos_A.loc[pos_A['is_sustain'] == True]
        team_B_sustain = pos_B.loc[pos_B['is_sustain'] == True]
        
        """---------------------------------"""
        

        team_A_maintain_possession = (team_A_maintain.duration.sum()/ (pos_A.duration.sum() + pos_B.duration.sum()))*100
        team_A_maintain_possession = np.round(team_A_maintain_possession, 2)
        
        team_B_maintain_possession = (team_B_maintain.duration.sum()/ (pos_A.duration.sum() + pos_B.duration.sum()))*100
        team_B_maintain_possession = np.round(team_B_maintain_possession, 2)
        
        
        team_A_buildup_possession = (team_A_buildup.duration.sum()/ (pos_A.duration.sum() + pos_B.duration.sum()))*100
        team_A_buildup_possession = np.round(team_A_buildup_possession, 2)

        team_B_buildup_possession = (team_B_buildup.duration.sum()/ (pos_A.duration.sum() + pos_B.duration.sum()))*100
        team_B_buildup_possession = np.round(team_B_buildup_possession, 2)
        
        team_A_sustain_possession = (team_A_sustain.duration.sum()/ (pos_A.duration.sum() + pos_B.duration.sum()))*100
        team_A_sustain_possession = np.round(team_A_sustain_possession, 2)

        team_B_sustain_possession = (team_B_sustain.duration.sum()/ (pos_A.duration.sum() + pos_B.duration.sum()))*100
        team_B_sustain_possession = np.round(team_B_sustain_possession, 2)
        
        """---------------------------------"""
        
        home_team.append(home_team_name)
        away_team.append(away_team_name)
        
        home_maintain.append(team_A_maintain_possession)
        away_maintain.append(team_B_maintain_possession)
        
        home_build.append(team_A_buildup_possession)
        away_build.append(team_B_buildup_possession)
        
        home_sustain.append(team_A_sustain_possession)
        away_sustain.append(team_B_sustain_possession)
        
        week.append(df_match.match_week.unique()[0])
        match.append(df_match.match_id.unique()[0])
        
    # Create a DataFrame to store possession calculations per match
    ppda = pd.DataFrame({
        "home_team": home_team,
        "away_team": away_team,
        "home_maintain": home_maintain,
        "away_maintain": away_maintain,
        "home_build": home_build,
        "away_build": away_build,
        "home_sustain": home_sustain,
        "away_sustain": away_sustain,
        "Match Week": week,
        "Match ID": match
    })

    ppda['home_maintain'] = ppda['home_maintain'].round(2)
    ppda['away_maintain'] = ppda['away_maintain'].round(2)

    ppda['home_build'] = ppda['home_build'].round(2)
    ppda['away_build'] = ppda['away_build'].round(2)

    ppda['home_sustain'] = ppda['home_sustain'].round(2)
    ppda['away_sustain'] = ppda['away_sustain'].round(2)

    home_data = ppda[['home_team', 'home_maintain', 'home_build', 'home_sustain']].copy()
    home_data.rename(columns = {'home_team': 'Team', 'home_maintain': 'Maintain (%)', 'home_build': 'Buildup (%)', 'home_sustain': 'Sustain (%)'}, inplace = True)

    away_data = ppda[['away_team', 'away_maintain', 'away_build', 'away_sustain']].copy()
    away_data.rename(columns = {'away_team': 'Team', 'away_maintain': 'Maintain (%)', 'away_build': 'Buildup (%)', 'away_sustain': 'Sustain (%)'}, inplace = True)

    result = pd.concat([home_data, away_data], ignore_index = True)

    average_mbs = result.groupby('Team')[['Maintain (%)', 'Buildup (%)', 'Sustain (%)']].mean().reset_index()

    average_mbs = average_mbs.sort_values(by='Maintain (%)', ascending=False)

    average_mbs['Maintain (%)'] = average_mbs['Maintain (%)'].round(2)
    average_mbs['Buildup (%)'] = average_mbs['Buildup (%)'].round(2)
    average_mbs['Sustain (%)'] = average_mbs['Sustain (%)'].round(2)

    return average_mbs

    
    