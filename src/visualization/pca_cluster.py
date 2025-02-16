# PCA and KMeans Clustering Analysis with Visualization for J League Teams

# Importing necessary libraries
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text  # For better label placement
import yaml

# ================================
# Step 1: Load Data
# ================================
# Reading J League metrics data from Excel file
# Load configuration from config.yaml
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

# File paths from config.yaml
input_file = config["paths"]["jleague_metrics"]
output_figure = config["paths"]["pca_clusters_figure"]

data = pd.read_excel(input_file)

# Selecting only numerical columns for PCA and clustering
data_excluding_selected = data.select_dtypes(include=['float64', 'int64'])

# Extracting team names separately for labeling
team_names = data['Team'].tolist()

# ================================
# Step 2: Data Preprocessing
# ================================
# Scaling data using MinMaxScaler
x = data_excluding_selected.values 
scaler = preprocessing.MinMaxScaler()
x_scaled = scaler.fit_transform(x)
X_norm = pd.DataFrame(x_scaled)

# ================================
# Step 3: Perform PCA
# ================================
pca = PCA(n_components = 2)
reduced = pd.DataFrame(pca.fit_transform(X_norm))

# ================================
# Step 4: Perform KMeans Clustering
# ================================
kmeans = KMeans(n_clusters=6, random_state=42)
kmeans = kmeans.fit(reduced)
labels = kmeans.predict(reduced)
clusters = kmeans.labels_.tolist()

# ================================
# Step 5: Prepare Data for Visualization
# ================================
# Adding cluster and team name columns to reduced dataframe
reduced['cluster'] = clusters
reduced['name'] = team_names
reduced.columns = ['x', 'y', 'cluster', 'name']

# ================================
# Step 6: Visualize Clusters
# ================================
# Set the visual style
sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 10))
fig.set_facecolor("#F5F5F5")
ax.set_facecolor("#FAF9F6")

# Scatter plot for all clusters
sns.scatterplot(x="x", y="y", hue="cluster", data=reduced, palette="Spectral", s=150, ax=ax, legend=False)

# Add team labels
texts = []
for _, row in reduced.iterrows():
    texts.append(ax.text(row['x'], row['y'], row['name'], fontsize=10, color='black',
                         bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.2")))

# Adjust overlapping labels
adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="->", color='grey', lw=0.8),
            expand_points=(1.4, 1.6), expand_text=(1.4, 1.6))

# Customize plot
ax.set_ylim(-2, 2)
ax.set_xlim(-2.5, 2.5)
ax.set_xlabel("Team Characteristics - Dimension 1", fontsize=15, labelpad=10)
ax.set_ylabel("Team Characteristics - Dimension 2", fontsize=15, labelpad=10)
ax.set_title("Playing Styles for Teams (J League)", fontsize=20, weight='bold', pad=20)
plt.tick_params(labelsize=12)

# Save the visualization
plt.savefig(output_figure, dpi=300, bbox_inches='tight')

# Display plot
plt.show()
