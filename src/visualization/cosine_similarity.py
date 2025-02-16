# PCA and KMeans Clustering Analysis with Cosine Similarity Heatmap for J League Teams

# ================================
# Step 1: Import Libraries
# ================================
import pandas as pd
import yaml
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text  # Adjust overlapping labels

# ================================
# Step 2: Load and Preprocess Data
# ================================
# Load J League metrics from Excel

# Load configuration from config.yaml
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

# File paths from config.yaml
input_file = config["paths"]["jleague_metrics"]
output_figure = config["paths"]["cosine_figure"]

data = pd.read_excel(input_file)
# Select only numerical columns
data_excluding_selected = data.select_dtypes(include=['float64', 'int64'])
# Extract team names for labels
team_names = data['Team'].tolist()

# Scale data using MinMaxScaler
x = data_excluding_selected.values
scaler = preprocessing.MinMaxScaler()
x_scaled = scaler.fit_transform(x)
X_norm = pd.DataFrame(x_scaled)

# ================================
# Step 3: Perform PCA and KMeans Clustering
# ================================
pca = PCA(n_components=2)
reduced = pd.DataFrame(pca.fit_transform(X_norm), columns=['x', 'y'])
kmeans = KMeans(n_clusters=6, random_state=42)
kmeans.fit(reduced)
clusters = kmeans.labels_.tolist()

# Add cluster and team name to reduced dataframe
reduced['cluster'] = clusters
reduced['name'] = team_names

# ================================
# Step 4: Compute Cosine Similarity and Plot Heatmap
# ================================
cosine_sim_matrix = pd.DataFrame(
    cosine_similarity(reduced[['x', 'y']]),
    index=reduced['name'],
    columns=reduced['name']
)

plt.figure(figsize=(10, 8))
sns.heatmap(
    cosine_sim_matrix, 
    cmap="Greens", 
    cbar=True, 
    linewidths=0, 
    xticklabels=True,  
    yticklabels=True
)
plt.title("Cosine Similarity Matrix", fontsize=15)
plt.savefig(output_figure, dpi=300, bbox_inches='tight')
plt.show()
