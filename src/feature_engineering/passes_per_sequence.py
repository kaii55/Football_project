import pandas as pd

def calculate_avg_passes_per_sequence(df):
    """
    Calculate Average Passes per Possession Sequence for each team.
    
    This metric computes the average number of passes during each possession.

    Args:
        df (pd.DataFrame): Processed J League events DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with Average Passes per Sequence for each team.
    """

    # Fill missing values and replace None or NaN with "Complete"
    df['pass.outcome.name'] = df['pass.outcome.name'].fillna("Complete").replace({None: "Complete"})

    df_events = df.copy()

    cd = df_events[['team.name', 'type.name', 'possession', 'possession_team.name', 'match_id']]

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

    result_df['Passes_per_sequence'] = result_df['Number_of_Passes']/ result_df['Number_of_Possession_Chains']

    result_df['Passes_per_sequence'] = result_df['Passes_per_sequence'].round(2)

    result_df = result_df.sort_values(by='Passes_per_sequence', ascending=False).reset_index(drop = True)

    result_df = result_df[['Team', 'Passes_per_sequence']]

    return result_df
