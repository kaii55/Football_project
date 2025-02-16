import pandas as pd
import numpy as np

def calculate_avg_verticality(df):
    """
    Calculate Average Verticality for each team.

    The ratio of forward progression to total pass distance, representing the directness of ball movement towards opponent’s goal.

    Args:
        df (pd.DataFrame): Processed J League events DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with Average Verticality for each team.
    """

    # Fill missing values and replace None or NaN with "Complete"
    df['pass.outcome.name'] = df['pass.outcome.name'].fillna("Complete").replace({None: "Complete"})

    df_events = df.copy()

    passes = df_events[(df_events['type.name'] == 'Pass') & (df_events['pass.outcome.name'] == 'Complete')]

    # Calculate forward progression and total distance of passes
    passes['forward_progress'] = passes['pass_end_x'] - passes['x']  # Forward movement (x-direction)
    passes['total_distance'] = np.sqrt((passes['pass_end_x'] - passes['x'])**2 + (passes['pass_end_y'] - passes['y'])**2)  # Euclidean distance

    # Calculate verticality as the ratio of forward progress to total distance
    passes['verticality'] = passes['forward_progress'] / passes['total_distance']

    # Ensure no division by zero (in case of any total_distance being zero)
    passes['verticality'] = passes['verticality'].fillna(0)

    # Aggregate verticality by team
    team_verticality = passes.groupby('team.name')['verticality'].mean().reset_index()
    team_verticality.columns = ['team.name', 'average_verticality']

    team_verticality.rename(columns = {'team.name': 'Team'}, inplace = True)

    team_verticality['average_verticality'] = team_verticality['average_verticality'].round(3)

    team_verticality = team_verticality.sort_values(by='average_verticality', ascending=False)
    
    return team_verticality 
