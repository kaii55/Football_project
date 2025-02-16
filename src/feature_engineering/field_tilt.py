import pandas as pd

def calculate_field_tilt(df):
    """
    Calculate Field Tilt (Attacking Third Possession).
    
    Field Tilt measures which team controls possession in the attacking third.
    
    Args:
        df (pd.DataFrame): Processed J League events DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with Field Tilt metrics.
    """

    # Fill missing values and replace None or NaN with "Complete"
    df['pass.outcome.name'] = df['pass.outcome.name'].fillna("Complete").replace({None: "Complete"})

    df_events = df.copy()

    match_ids = df_events["match_id"].unique()

    home_team = []
    away_team = []
    home_attt = []
    away_attt = []

    ppda = pd.DataFrame()

    for match_id in match_ids:
        df_match = df_events[df_events["match_id"] == match_id]
        
        
        # Identify home and away teams from the match dataset
        home_team_name = df_match['home_team'].unique()[0]
        away_team_name = df_match['away_team'].unique()[0]
        
        
        
        def is_att_third(endX):
            if endX >= 80.0:
                return True  
            else:
                return False
            
            
        pass_data = df_match.loc[df_match['type.name'] == 'Pass']
        
        pass_data["is_att_third"] = pass_data.apply(lambda row : is_att_third(row['pass_end_x']), axis = 1)
        pass_data_att_third = pass_data.loc[pass_data['is_att_third'] == True]
        
        
        
        team1_att_third_pass_data = pass_data_att_third.loc[pass_data_att_third['team.name'] == home_team_name]
        team2_att_third_pass_data = pass_data_att_third.loc[pass_data_att_third['team.name'] == away_team_name]
        
        home_team.append(home_team_name)
        away_team.append(away_team_name)

        
        home_attt.append(team1_att_third_pass_data.shape[0])
        away_attt.append(team2_att_third_pass_data.shape[0])
        

    ppda['home_team'] = home_team
    ppda['away_team'] = away_team

    ppda['home_attt'] = home_attt
    ppda['away_attt'] = away_attt
    
    ppda['home_tilt'] = ppda['home_attt']/ (ppda['home_attt'] + ppda['away_attt'])
    ppda['away_tilt'] = ppda['away_attt']/ (ppda['home_attt'] + ppda['away_attt'])

    ppda['home_tilt'] = ppda['home_tilt'].round(2) * 100
    ppda['away_tilt'] = ppda['away_tilt'].round(2) * 100


    home_data = ppda[['home_team', 'home_tilt']].copy()
    home_data.rename(columns = {'home_team': 'Team', 'home_tilt': 'Field_tilt'}, inplace = True)

    away_data = ppda[['away_team', 'away_tilt']].copy()
    away_data.rename(columns = {'away_team': 'Team', 'away_tilt': 'Field_tilt'}, inplace = True)

    result = pd.concat([home_data, away_data], ignore_index = True)

    average_FT = result.groupby('Team')['Field_tilt'].mean().reset_index()


    average_FT['Field_tilt'] = average_FT['Field_tilt'].round(2)

    average_FT = average_FT.sort_values(by='Field_tilt', ascending=True)


    return average_FT