import pandas as pd
from possession import calculate_possession
from ppda import calculate_ppda
from field_tilt import calculate_field_tilt
from maintain_buildup_sustain import calculate_maintain_buildup_sustain
from speed_metrics import calculate_speed_metrics
from passes_per_sequence import calculate_avg_passes_per_sequence
from attacking_passes_per_sequence import calculate_avg_attacking_passes_per_sequence
from verticality import calculate_avg_verticality
from defensive_height import calculate_avg_defensive_height
from attacks import calculate_buildup_and_direct_attacks
from attacks_under_10_passes import calculate_buildup_and_direct_attacks_under_10_passes


# File paths
input_parquet = "/Users/aritramajumdar/Desktop/Football_project/data/processed/J_League_data.parquet"
output_file = "/Users/aritramajumdar/Desktop/Football_project/data/processed/jleague_metrics.xlsx"

# Load the processed Parquet file
df = pd.read_parquet(input_parquet)

# Calculate metrics
possession = calculate_possession(df)
ppda = calculate_ppda(df)
field_tilt = calculate_field_tilt(df)
mbs = calculate_maintain_buildup_sustain(df)
speed_metrics = calculate_speed_metrics(df)
avg_passes = calculate_avg_passes_per_sequence(df)
avg_attacking_passes = calculate_avg_attacking_passes_per_sequence(df)
avg_verticality = calculate_avg_verticality(df)
avg_defensive_height = calculate_avg_defensive_height(df)
attacks = calculate_buildup_and_direct_attacks(df)
attacks_under_10 = calculate_buildup_and_direct_attacks_under_10_passes(df)


# Merge all metrics into a single DataFrame
metrics_df = (
    possession
    .merge(ppda, on='Team', how='left')
    .merge(field_tilt, on='Team', how='left')
    .merge(mbs, on='Team', how='left')
    .merge(speed_metrics, on='Team', how='left')
    .merge(avg_passes, on='Team', how='left')
    .merge(avg_attacking_passes, on='Team', how='left')
    .merge(avg_verticality, on='Team', how='left')
    .merge(avg_defensive_height, on='Team', how='left')
    .merge(attacks, on='Team', how='left')
    .merge(attacks, on='Team', how='left')
)

# Save the metrics to an Excel file
metrics_df.to_excel(output_file, index=False)
print(f"✅ All metrics saved to {output_file}")
