import pandas as pd
from possession import calculate_possession
from ppda import calculate_ppda

# File paths
input_parquet = "/Users/aritramajumdar/Desktop/Football_project/data/processed/J_League_data.parquet"
output_file = "/Users/aritramajumdar/Desktop/Football_project/data/processed/jleague_metrics.xlsx"

# Load the processed Parquet file
df = pd.read_parquet(input_parquet)

# Calculate metrics
possession = calculate_possession(df)
ppda = calculate_ppda(df)
field_tilt = calculate_field_tilt(df)


# Merge metrics into a single DataFrame
metrics_df = (
    possession
    .merge(ppda, on='Team', how='outer')
    .merge(field_tilt, on='Team', how='left')
)

# Save the metrics to an Excel file
metrics_df.to_excel(output_file, index=False)
print(f"✅ All metrics saved to {output_file}")
