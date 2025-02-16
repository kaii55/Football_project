import pandas as pd
import numpy as np

def calculate_speed_metrics(df):
    """
    Calculate Speed and Direct Speed for each team.
    
    Speed: The speed of ball movement during a possession sequence. 
    Direct Speed: The average speed of ball progression towards the opponent’s goal.
    
    Args:
        df (pd.DataFrame): Processed J League events DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with Speed and Direct Speed metrics.
    """

    # Fill missing values and replace None or NaN with "Complete"
    df['pass.outcome.name'] = df['pass.outcome.name'].fillna("Complete").replace({None: "Complete"})

    df_events = df.copy()

    match_ids = df_events["match_id"].unique()

    chains_data = []

    for match_id in match_ids:
        df_match = df_events[df_events["match_id"] == match_id]
        
        df_match['Time'] = df_match['minute'] * 60 + df_match['second']
        df_match['Time_diff'] = df_match['Time'].diff()
        df_match['Time_diff'].fillna(0, inplace = True)
        df_match["Time_diff"] = df_match["Time_diff"].shift(-1)
        
        df_match['ordinate'] = np.sqrt(df_match['x']**2 + df['y']**2)
        df_match['distance'] = np.abs(df_match['ordinate'].diff())
        df_match['distance'].fillna(0, inplace = True)
        df_match["distance"] = df_match["distance"].shift(-1)
        
        chains = pd.DataFrame()
        for v in df_match.possession.unique():
            chain = df_match.loc[df_match["possession"] == v]
            chain['Sequence Time'] = chain['Time_diff'].sum()
            
            chain['Progress'] = chain.iloc[-1].x - chain.iloc[0].x
            
            chain['Length'] = chain['distance'].sum()
            
            
            chain['Speed'] = chain['Length'] / chain['Sequence Time']
            chain['Direct Speed'] = chain['Progress'] / chain['Sequence Time']
            
            
            if chain.shape[0] >= 4:  
                
                chains = pd.concat([chains, chain], ignore_index=True)
            
        chains_data.append(chains)
            
    chains_data = pd.concat(chains_data) 

    ch = chains_data.groupby(['match_id', 'possession', 'possession_team.name']).agg({
    'Speed': 'first',           # Take the first value of speed for each group
    'Direct Speed': 'first'     # Take the first value of direct_speed for each group
    }).reset_index()

    ch_pos = ch.loc[ch["Direct Speed"] >= 0]
    pass_counts = chains_data[chains_data['type.name'] == 'Pass'].groupby(['possession','possession_team.name', 'match_id'])['type.name'].count().reset_index()
    r = ch_pos.merge(pass_counts, on=['match_id', 'possession', 'possession_team.name'], how = 'left')
    r_filter = r[~np.isinf(r['Direct Speed'])]
    a = r_filter.groupby(['possession_team.name']).agg({
        'Direct Speed': 'mean',           # Take the first value of speed for each group
        'Speed': 'mean',
    }).reset_index()


    a.columns = ['Team', 'Direct Speed Upfield(m/s)', 'Speed']

    return a

