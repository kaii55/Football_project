import pandas as pd

def calculate_avg_pressure(df):
    """
    Calculate Average Pressure per Possession for each team.

    Args:
        df (pd.DataFrame): Processed J League events DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with Average Pressure per Team.
    """


    # Fill missing values and replace None or NaN with "Complete"
    df['pass.outcome.name'] = df['pass.outcome.name'].fillna("Complete").replace({None: "Complete"})

    df_events = df.copy()

    match_ids = df_events["match_id"].unique()

    # Lists to store match-level statistics
    home_team = []
    away_team = []

    home_possession_home_pressure = []
    home_possession_away_pressure = []

    away_possession_away_pressure = []
    away_possession_home_pressure = []

    week = []
    match = []

    for match_id in match_ids:
        df_match = df_events[df_events["match_id"] == match_id]
        
        # Identify home and away teams for this match
        home_team_name = df_match['home_team'].unique()[0]
        away_team_name = df_match['away_team'].unique()[0]
        
        # Store team details
        home_team.append(home_team_name)
        away_team.append(away_team_name)
        

        ## --- PRESSURE EVENTS COUNT --- ##

        # When home team is in possession
        df_home_possession = df_match[df_match['possession_team.name'] == home_team_name]
        
        home_possession_home_press = df_home_possession[
            (df_home_possession['type.name'] == "Pressure") & (df_home_possession['team.name'] == home_team_name)
        ].shape[0]
        
        home_possession_away_press = df_home_possession[
            (df_home_possession['type.name'] == "Pressure") & (df_home_possession['team.name'] == away_team_name)
        ].shape[0]
        
        # When away team is in possession
        df_away_possession = df_match[df_match['possession_team.name'] == away_team_name]
        
        away_possession_away_press = df_away_possession[
            (df_away_possession['type.name'] == "Pressure") & (df_away_possession['team.name'] == away_team_name)
        ].shape[0]
        
        away_possession_home_press = df_away_possession[
            (df_away_possession['type.name'] == "Pressure") & (df_away_possession['team.name'] == home_team_name)
        ].shape[0]

        # Append computed values to respective lists
        home_possession_home_pressure.append(home_possession_home_press)
        home_possession_away_pressure.append(home_possession_away_press)
        away_possession_away_pressure.append(away_possession_away_press)
        away_possession_home_pressure.append(away_possession_home_press)
        
        week.append(df_match.match_week.unique()[0])
        match.append(df_match.match_id.unique()[0])

    # Create a DataFrame with structured data
    pressure_data = pd.DataFrame({
        "Match Week": week,
        "Match ID": match,
        "home_team": home_team,
        "away_team": away_team,
        "home_possession_home_pressure": home_possession_home_pressure,
        "home_possession_away_pressure": home_possession_away_pressure,
        "away_possession_away_pressure": away_possession_away_pressure,
        "away_possession_home_pressure": away_possession_home_pressure
    })

    p_data = pressure_data[['home_team', 'away_team', 'home_possession_away_pressure', 'away_possession_home_pressure']]

    p_data = p_data.rename(columns={ 
                     'home_possession_away_pressure': 'Away Pressure', 
                     'away_possession_home_pressure': 'Home Pressure'})


    home_data = p_data[['home_team', 'Home Pressure']].copy()
    home_data.rename(columns = {'home_team': 'Team', 'Home Pressure': 'Pressure'}, inplace = True)

    away_data = p_data[['away_team', 'Away Pressure']].copy()
    away_data.rename(columns = {'away_team': 'Team', 'Away Pressure': 'Pressure'}, inplace = True)

    result = pd.concat([home_data, away_data], ignore_index = True)

    average_pressure = result.groupby('Team')['Pressure'].mean().reset_index()

    average_pressure = average_pressure.sort_values(by='Pressure', ascending=True)
    average_pressure['Pressure'] = average_pressure['Pressure'].round(2)

    average_pressure


