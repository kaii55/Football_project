import pandas as pd

def calculate_buildup_and_direct_attacks_under_10_passes(df):
    """
    Calculate Buildup Attacks and Direct Attacks (with fewer than 10 passes) for each team.

    - Buildup Attacks: The number of open-play sequences consisting of 10+ passes 
    that either result in a shot or include at least one touch inside the opponent’s penalty box.
    - Direct Attacks (<10 passes): A variation of Direct Attack where the sequence is completed 
    in fewer than 10 passes.

    Args:
        df (pd.DataFrame): Processed J League events DataFrame.

    Returns:
        pd.DataFrame: DataFrame with counts of Buildup and Direct Attacks per team.
    """

    # Fill missing values and replace None or NaN with "Complete"
    df['pass.outcome.name'] = df['pass.outcome.name'].fillna("Complete").replace({None: "Complete"})

    df['play_pattern.name'] = df['play_pattern.name'].where(
    df['play_pattern.name'].isin(['From Corner', 'From Free Kick']), 'Regular Play'
    )   

    df_events = df.copy()

    match_ids = df_events["match_id"].unique()


    chains_data_att = []
    chains_data_normal = []


    for match_id in match_ids:
        df_match = df_events[df_events["match_id"] == match_id]
        
        
        # Identify home and away teams from the match dataset
        home_team_name = df_match['home_team'].unique()[0]
        away_team_name = df_match['away_team'].unique()[0]
        
        
        chains_normal = pd.DataFrame()

        for v in df_match.possession.unique():
            chain = df_match.loc[df_match["possession"] == v]

            try:
                if chain.shape[0] > 2:  # Ensure there are enough events to check iloc[-2]
                    last_event = chain.iloc[-1]

                    # If the last event is a goalkeeper action, check the second-last event instead
                    if last_event['type.name'] == 'Goal Keeper':
                        final_x = chain.iloc[-2].x
                        final_y = chain.iloc[-2].y
                    else:
                        final_x = last_event.x
                        final_y = last_event.y

                    # Apply the filtering conditions
                    if ((chain['type.name'].value_counts().get('Pass', 0) >= 10) and 
                        (chain.iloc[0]['type.name'] == 'Pass') and 
                        ("Regular Play" in chain["play_pattern.name"].values) and 
                        ("Shot" in chain["type.name"].values)) or \
                    ((chain['type.name'].value_counts().get('Pass', 0) >= 10) and 
                        (chain.iloc[0]['type.name'] == 'Pass') and 
                        ("Regular Play" in chain["play_pattern.name"].values) and 
                        (final_x >= 102.0) and (18.0 < final_y < 62.0)):

                        chains_normal = pd.concat([chains_normal, chain])  # Use concat instead of append

            except Exception as e:
                pass  # Avoid breaking the loop on errors

                
            chains_att = pd.DataFrame()

            for v in df_match.possession.unique():
                chain = df_match.loc[df_match["possession"] == v]

                try:
                    if chain.shape[0] > 2:  # Ensure enough events exist
                        last_event = chain.iloc[-1]

                        # If the last event is a goalkeeper action, use the second-last event instead
                        if last_event['type.name'] == 'Goal Keeper':
                            final_x = chain.iloc[-2].x
                            final_y = chain.iloc[-2].y
                        else:
                            final_x = last_event.x
                            final_y = last_event.y

                        # Apply the filtering conditions
                        if ((chain.iloc[0]['type.name'] == 'Pass') and 
                            (chain['type.name'].value_counts().get('Pass', 0) < 10) and 
                            ("Regular Play" in chain["play_pattern.name"].values) and 
                            (chain.iloc[0].x < 60.0) and 
                            (final_x >= (chain.iloc[0].x + (120.0 - chain.iloc[0].x)/2)) and 
                            ("Shot" in chain["type.name"].values)) or \
                        ((chain.iloc[0]['type.name'] == 'Pass') and 
                            (chain['type.name'].value_counts().get('Pass', 0) < 10) and 
                            ("Regular Play" in chain["play_pattern.name"].values) and 
                            (chain.iloc[0].x < 60.0) and 
                            (final_x >= (chain.iloc[0].x + (120.0 - chain.iloc[0].x)/2)) and 
                            (final_x >= 102.0) and (18.0 < final_y < 62.0)):

                            chains_att = pd.concat([chains_att, chain])  # Use pd.concat instead of .append()

                except Exception as e:
                    pass  # Avoid breaking the loop on errors

            
        chains_data_normal.append(chains_normal)
        chains_data_att.append(chains_att)
            
    chains_data_normal = pd.concat(chains_data_normal)
    chains_data_att = pd.concat(chains_data_att)

    team_possession_counts_normal = chains_data_normal.groupby(['possession_team.name', 'match_id'])['possession'].nunique().reset_index()
    table = team_possession_counts_normal.groupby('possession_team.name')['possession'].sum().reset_index()
    team_possession_counts_att = chains_data_att.groupby(['possession_team.name', 'match_id'])['possession'].nunique().reset_index()
    table1 = team_possession_counts_att.groupby('possession_team.name')['possession'].sum().reset_index()
    table1.rename(columns = {'possession': 'possesion_chain_att'}, inplace = True)

    data = table.merge(table1, on='possession_team.name')
    
    data.rename(columns = {'possession': 'Buildup Attacks', 
                    'possesion_chain_att': 'Direct Attacks_10'}, inplace = True)

    data.rename(columns = {'possession_team.name': 'Team'}, inplace = True)

    return data


    


