import pandas as pd

def calculate_ppda(df):
    """
    Calculate Passes per Defensive Action (PPDA).
    
    Args:
        df (pd.DataFrame): Processed J League events DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with PPDA metrics.
    """


    # Fill missing values and replace None or NaN with "Complete"
    df['pass.outcome.name'] = df['pass.outcome.name'].fillna("Complete").replace({None: "Complete"})
    df['duel.type.name'] = df['duel.type.name'].fillna("")


    df_events = df.copy()

    match_ids = df_events["match_id"].unique()

    home_team = []
    away_team = []
    home_ppda = []
    away_ppda = []

    ppda = pd.DataFrame()

    # Iterate over each match
    for match_id in match_ids:
        df_match = df_events[df_events["match_id"] == match_id]
        
        # Identify home and away teams
        home_team_name = df_match['home_team'].unique()[0]
        away_team_name = df_match['away_team'].unique()[0]
        
        # Filter events in opponent's half (x > 48.0)
        df_match = df_match.loc[df_match['x'] > 48.0]

        # Split data by team
        team1 = df_match.loc[df_match['team.name'] == home_team_name]
        team2 = df_match.loc[df_match['team.name'] == away_team_name]

        # Filter Passes
        team1_pass = team1.loc[team1['type.name'] == 'Pass']
        team2_pass = team2.loc[team2['type.name'] == 'Pass']

        # Filter Successful Passes
        team1_pass_succ = team1_pass.loc[team1_pass['pass.outcome.name'] == 'Complete']
        team2_pass_succ = team2_pass.loc[team2_pass['pass.outcome.name'] == 'Complete']

        team1_defensive_actions = pd.concat([
            team1.loc[team1['type.name'].isin(['Interception', 'Foul Committed', 'Block'])],
            team1.loc[team1['duel.type.name'] == "Tackle"]
        ]).drop_duplicates().reset_index(drop=True)
        
        team2_defensive_actions = pd.concat([
            team2.loc[team2['type.name'].isin(['Interception', 'Foul Committed', 'Block'])],
            team2.loc[team2['duel.type.name'] == "Tackle"]
        ]).drop_duplicates().reset_index(drop=True)


        team1_def_count = max(team1_defensive_actions.shape[0], 1)  # Avoid ZeroDivisionError
        team2_def_count = max(team2_defensive_actions.shape[0], 1)  # Avoid ZeroDivisionError

        home_PPDA = team2_pass_succ.shape[0] / team1_def_count
        away_PPDA = team1_pass_succ.shape[0] / team2_def_count

        # Append computed values
        home_team.append(home_team_name)
        away_team.append(away_team_name)
        home_ppda.append(home_PPDA)
        away_ppda.append(away_PPDA)

        
        
    ppda['home_team'] = home_team
    ppda['away_team'] = away_team
    ppda['home_ppda'] = home_ppda
    ppda['away_ppda'] = away_ppda

    ppda['home_ppda'] = ppda['home_ppda'].round(3)
    ppda['away_ppda'] = ppda['away_ppda'].round(3)

    home_data = ppda[['home_team', 'home_ppda']].copy()
    home_data.rename(columns = {'home_team': 'Team', 'home_ppda': 'PPDA'}, inplace = True)

    away_data = ppda[['away_team', 'away_ppda']].copy()
    away_data.rename(columns = {'away_team': 'Team', 'away_ppda': 'PPDA'}, inplace = True)

    result = pd.concat([home_data, away_data], ignore_index = True)

    average_ppda = result.groupby('Team')['PPDA'].mean().reset_index()

    average_ppda = average_ppda.sort_values(by='PPDA', ascending=True)
    average_ppda['PPDA'] = average_ppda['PPDA'].round(3)

    return average_ppda