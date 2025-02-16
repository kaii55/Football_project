import pandas as pd

def calculate_possession(df):
    """
    Calculate possession percentage for each team.
    
    Args:
        df (pd.DataFrame): Processed J League events DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with possession metrics.
    """

    df_events = df.copy()

    match_ids = df_events["match_id"].unique()

    # Initialize lists to store computed metrics for each match
    home_team = []
    away_team = []
    home_possession = []
    away_possession = []
    week = []
    match = []

    # Process each match individually
    for match_id in match_ids:
        df_match = df_events[df_events["match_id"] == match_id]

        # Identify home and away teams from the match dataset
        home_team_name = df_match['home_team'].unique()[0]
        away_team_name = df_match['away_team'].unique()[0]

        # Create copies for possession calculation
        pos_A = df_match[df_match['team.name'] == home_team_name]
        pos_B = df_match[df_match['team.name'] == away_team_name]

        # Extract unique team names
        team1_name = home_team_name
        team2_name = away_team_name

        # Extract pass events for possession calculation
        pos_A_pass = pos_A[pos_A['type.name'] == 'Pass']
        pos_B_pass = pos_B[pos_B['type.name'] == 'Pass']

        # Compute possession percentage for each team
        total_passes = pos_A_pass.shape[0] + pos_B_pass.shape[0]
        pos_A_mom = (pos_A_pass.shape[0] / total_passes) * 100
        pos_B_mom = (pos_B_pass.shape[0] / total_passes) * 100

        # Append match data to respective lists
        home_team.append(team1_name)
        away_team.append(team2_name)
        home_possession.append(pos_A_mom)
        away_possession.append(pos_B_mom)
        week.append(df_match.match_week.unique()[0])
        match.append(df_match.match_id.unique()[0])

    # Create a DataFrame to store possession calculations per match
    possession_df = pd.DataFrame({
        "home_team": home_team,
        "away_team": away_team,
        "home_possession": home_possession,
        "away_possession": away_possession,
        "Match Week": week,
        "Match ID": match
    })

    # Convert match-level data into team-level aggregation
    home_data = possession_df[['home_team', 'home_possession']].rename(columns={'home_team': 'Team', 'home_possession': 'Possession'})
    away_data = possession_df[['away_team', 'away_possession']].rename(columns={'away_team': 'Team', 'away_possession': 'Possession'})

    # Combine home and away team data
    result = pd.concat([home_data, away_data], ignore_index=True)

    # Compute the average possession percentage per team across matches
    average_possession = result.groupby('Team')['Possession'].mean().reset_index()

    # Sort teams based on possession values in descending order
    average_possession = average_possession.sort_values(by='Possession', ascending=False).round(2).reset_index(drop = True)

    return average_possession


