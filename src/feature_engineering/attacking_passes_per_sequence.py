import pandas as pd

def calculate_avg_attacking_passes_per_sequence(df):
    """
    Calculate Average Attacking Passes per Possession Sequence for each team.

    Attacking Passes are passes made in the opponent's half.

    Args:
        df (pd.DataFrame): Processed J League events DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with Average Attacking Passes per Sequence for each team.
    """

    # Fill missing values and replace None or NaN with "Complete"
    df['pass.outcome.name'] = df['pass.outcome.name'].fillna("Complete").replace({None: "Complete"})

    df_events = df.copy()

    match_ids = df_events["match_id"].unique()

    chains_data = []

    for match_id in match_ids:
        df_match = df_events[df_events["match_id"] == match_id]
        
        chains = pd.DataFrame()
        for v in df_match.possession.unique():
            chain = df_match.loc[df_match["possession"] == v]
            if ("Shot" in chain["type.name"].values) and (chain.shape[0] >= 3):
                chains = pd.concat([chains, chain], ignore_index=True)
        
        chains_data.append(chains)
        
    chains_data = pd.concat(chains_data) 

    cd = chains_data.copy()

    cd = chains_data[['team.name', 'type.name', 'possession', 'possession_team.name', 'match_id']]


    possession_chain_counts = cd.groupby(['possession_team.name', 'match_id'])['possession'].nunique().reset_index()
    # Calculate the event counts per team
    event_counts = cd.groupby(['possession_team.name', 'match_id'])['type.name'].count().reset_index()

    # Calculate the pass counts per team
    pass_counts = cd[cd['type.name'] == 'Pass'].groupby(['possession_team.name', 'match_id'])['type.name'].count().reset_index()

    possession_chain_counts = possession_chain_counts.groupby('possession_team.name')['possession'].sum().reset_index()

    event_counts = event_counts.groupby('possession_team.name')['type.name'].sum().reset_index()

    pass_counts = pass_counts.groupby('possession_team.name')['type.name'].sum().reset_index()

    # Rename the columns for clarity
    possession_chain_counts.columns = ['Team', 'Number_of_Possession_Chains']
    event_counts.columns = ['Team', 'Number_of_Events']
    pass_counts.columns = ['Team', 'Number_of_Passes']

    # Merge the DataFrames
    result_df = possession_chain_counts.merge(event_counts, on='Team')
    result_df = result_df.merge(pass_counts, on='Team')

    # Display the result
    result_df['Att. Passes_per_sequence'] = result_df['Number_of_Passes']/ result_df['Number_of_Possession_Chains']
    result_df['Att. Passes_per_sequence'] = result_df['Att. Passes_per_sequence'].round(2)

    result_df = result_df.sort_values(by='Att. Passes_per_sequence', ascending=False)

    result_df = result_df[['Team', 'Att. Passes_per_sequence']]

    return result_df

