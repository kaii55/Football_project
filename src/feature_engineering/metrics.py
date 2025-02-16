import pandas as pd
from possession import calculate_possession
from ppda import calculate_ppda
from field_tilt import calculate_field_tilt
from maintain_buildup_sustain import calculate_maintain_buildup_sustain
from speed_metrics import calculate_speed_metrics
from passes_per_sequence import calculate_avg_passes_per_sequence

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

# Merge all metrics into a single DataFrame
metrics_df = (
    possession
    .merge(ppda, on='Team', how='left')
    .merge(field_tilt, on='Team', how='left')
    .merge(mbs, on='Team', how='left')
    .merge(speed_metrics, on='Team', how='left')
    .merge(avg_passes, on='team.name', how='left')
)

# Save the metrics to an Excel file
metrics_df.to_excel(output_file, index=False)
print(f"✅ All metrics saved to {output_file}")
