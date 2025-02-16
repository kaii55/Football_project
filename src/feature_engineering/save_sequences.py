import pandas as pd
import yaml

with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

input_parquet = config["paths"]["output"]
output_file = config["paths"]["output_sequence"]

df = pd.read_parquet(input_parquet)

# Fill missing values and replace None or NaN with "Complete"
df['pass.outcome.name'] = df['pass.outcome.name'].fillna("Complete").replace({None: "Complete"})

df_events = df.copy()

match_ids = df_events["match_id"].unique()

home_team = []
away_team = []

home_chain_normal = []
home_chain_shot = []
home_chain_att_t = []
home_chain_in_box = []

away_chain_normal = []
away_chain_shot = []
away_chain_att_t = []
away_chain_in_box = []

sequences = pd.DataFrame()

for match_id in match_ids:
    df_match = df_events[df_events["match_id"] == match_id]
    
    home_team_name = df_match['home_team'].unique()[0]
    away_team_name = df_match['away_team'].unique()[0]
    
    home_chain = df_match.loc[df_match['team.name'] == home_team_name]
    away_chain = df_match.loc[df_match['team.name'] == away_team_name]
    
    """Home Team Sequences""" 
    home_chains = pd.DataFrame()
    for v in home_chain.possession.unique():
        chain = home_chain.loc[home_chain["possession"] == v]
        if chain.shape[0] > 2:
            home_chains = pd.concat([home_chains, chain], ignore_index=True)
    
    home_chains_att = pd.DataFrame()
    for v in home_chain.possession.unique():
        chain = home_chain.loc[home_chain["possession"] == v]
        if "Shot" in chain["type.name"].values and chain.shape[0] > 2:
            home_chains_att = pd.concat([home_chains_att, chain], ignore_index=True)
    
    home_chains_att_t = pd.DataFrame()
    for v in home_chain.possession.unique():
        chain = home_chain.loc[home_chain["possession"] == v]
        if chain.iloc[-1].x > 80.0 and chain.shape[0] > 2:
            home_chains_att_t = pd.concat([home_chains_att_t, chain], ignore_index=True)
    
    home_chains_in_box = pd.DataFrame()
    for v in home_chain.possession.unique():
        chain = home_chain.loc[home_chain["possession"] == v]
        if chain.shape[0] > 2:
            last_event = chain.iloc[-1]
            if last_event['type.name'] == 'Goal Keeper' and chain.shape[0] > 2:
                second_last_event = chain.iloc[-2]
                if second_last_event.x > 102.0 and 18.0 < second_last_event.y < 62.0:
                    home_chains_in_box = pd.concat([home_chains_in_box, chain], ignore_index=True)
            else:
                if last_event.x > 102.0 and 18.0 < last_event.y < 62.0:
                    home_chains_in_box = pd.concat([home_chains_in_box, chain], ignore_index=True)
    
    """Away Team Sequences""" 
    away_chains = pd.DataFrame()
    for v in away_chain.possession.unique():
        chain = away_chain.loc[away_chain["possession"] == v]
        if chain.shape[0] > 2:
            away_chains = pd.concat([away_chains, chain], ignore_index=True)
    
    away_chains_att = pd.DataFrame()
    for v in away_chain.possession.unique():
        chain = away_chain.loc[away_chain["possession"] == v]
        if "Shot" in chain["type.name"].values and chain.shape[0] > 2:
            away_chains_att = pd.concat([away_chains_att, chain], ignore_index=True)
    
    away_chains_att_t = pd.DataFrame()
    for v in away_chain.possession.unique():
        chain = away_chain.loc[away_chain["possession"] == v]
        if chain.iloc[-1].x > 80.0 and chain.shape[0] > 2:
            away_chains_att_t = pd.concat([away_chains_att_t, chain], ignore_index=True)
    
    away_chains_in_box = pd.DataFrame()
    for v in away_chain.possession.unique():
        chain = away_chain.loc[away_chain["possession"] == v]
        if chain.shape[0] > 2:
            last_event = chain.iloc[-1]
            if last_event['type.name'] == 'Goal Keeper' and chain.shape[0] > 2:
                second_last_event = chain.iloc[-2]
                if second_last_event.x > 102.0 and 18.0 < second_last_event.y < 62.0:
                    away_chains_in_box = pd.concat([away_chains_in_box, chain], ignore_index=True)
            else:
                if last_event.x > 102.0 and 18.0 < last_event.y < 62.0:
                    away_chains_in_box = pd.concat([away_chains_in_box, chain], ignore_index=True)
    
    # Collect lengths of sequences
    home_chain_normal.append(len(home_chains.possession.unique()) if not home_chains.empty else 0)
    home_chain_shot.append(len(home_chains_att.possession.unique()) if not home_chains_att.empty else 0)
    home_chain_att_t.append(len(home_chains_att_t.possession.unique()) if not home_chains_att_t.empty else 0)
    home_chain_in_box.append(len(home_chains_in_box.possession.unique()) if not home_chains_in_box.empty else 0)
    
    away_chain_normal.append(len(away_chains.possession.unique()) if not away_chains.empty else 0)
    away_chain_shot.append(len(away_chains_att.possession.unique()) if not away_chains_att.empty else 0)
    away_chain_att_t.append(len(away_chains_att_t.possession.unique()) if not away_chains_att_t.empty else 0)
    away_chain_in_box.append(len(away_chains_in_box.possession.unique()) if not away_chains_in_box.empty else 0)
    
    home_team.append(home_team_name)
    away_team.append(away_team_name)

# Create sequences DataFrame
sequences['home_team'] = home_team
sequences['away_team'] = away_team
sequences['home_chain_normal'] = home_chain_normal
sequences['home_chain_shot'] = home_chain_shot
sequences['home_chain_att_third'] = home_chain_att_t
sequences['home_chain_in_box'] = home_chain_in_box
sequences['away_chain_normal'] = away_chain_normal
sequences['away_chain_shot'] = away_chain_shot
sequences['away_chain_att_third'] = away_chain_att_t
sequences['away_chain_in_box'] = away_chain_in_box  

# Save to Parquet
sequences.to_excel(output_file, index=False)
print(f"✅ Sequences saved to {output_file}")
