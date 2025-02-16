import json
import pandas as pd
import yaml

# Load configuration from config.yaml
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

# File paths from config
events_path = config["paths"]["events"]
matches_path = config["paths"]["matches"]
output_path = config["paths"]["output"]

def load_json(file_path):
    """Load JSON file into a Pandas DataFrame."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict):
        return pd.json_normalize(data)
    else:
        raise ValueError("Invalid JSON structure.")

def extract_coordinates(df, column_name, x_col, y_col):
    """Extract x and y coordinates from list columns."""
    df[x_col] = df[column_name].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)
    df[y_col] = df[column_name].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None)
    return df

def preprocess_events(events_df):
    """Preprocess events data."""
    # Drop unnecessary columns
    events_df = events_df.drop(columns=['related_events', 'tactics.lineup'], errors='ignore')

    # Extract coordinates
    events_df = extract_coordinates(events_df, 'location', 'x', 'y')
    events_df = extract_coordinates(events_df, 'pass.end_location', 'pass_end_x', 'pass_end_y')
    events_df = extract_coordinates(events_df, 'carry.end_location', 'carry_end_x', 'carry_end_y')
    events_df = extract_coordinates(events_df, 'shot.end_location', 'shot_end_x', 'shot_end_y')
    events_df = extract_coordinates(events_df, 'goalkeeper.end_location', 'goalkeeper_end_x', 'goalkeeper_end_y')

    # Drop original list columns
    columns_to_drop = ['location', 'pass.end_location', 'carry.end_location',
                       'shot.end_location', 'goalkeeper.end_location']
    events_df = events_df.drop(columns=columns_to_drop, errors='ignore')

    return events_df

def preprocess_matches(matches_df):
    """Preprocess matches data."""
    matches_df = matches_df.rename(columns={
        'home_team.home_team_name': 'home_team',
        'away_team.away_team_name': 'away_team'
    })
    return matches_df[['match_id', 'home_team', 'away_team', 'match_week', 'home_score', 'away_score']]

def merge_events_matches(events_df, matches_df):
    """Merge events with match information."""
    merged_df = events_df.merge(
        matches_df,
        on='match_id',
        how='left'
    )
    return merged_df

def save_as_parquet(df, output_path):
    """Save DataFrame as Parquet file."""
    df.to_parquet(output_path, index=False, engine='pyarrow')
    print(f"✅ Processed data saved at {output_path}")

if __name__ == "__main__":
    print("🚀 Starting J League Data Preprocessing...")

    # Load data
    events_df = load_json(events_path)
    matches_df = load_json(matches_path)

    # Preprocess
    events_df = preprocess_events(events_df)
    matches_df = preprocess_matches(matches_df)

    # Merge
    merged_df = merge_events_matches(events_df, matches_df)

    # Save
    save_as_parquet(merged_df, output_path)

    print("✅ J League Data Preprocessing Completed.")
