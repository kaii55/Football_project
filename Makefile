# ==========================
# Installation Commands
# ==========================
install:
	pip install -r requirements.txt

# ==========================
# Testing
# ==========================
test:
	pytest tests/

# ==========================
# Jupyter Notebooks
# ==========================
run-notebook:
	jupyter notebook

# ==========================
# Run Visualizations
# ==========================
pca-cluster:
	python src/visualization/pca_cluster.py

cosine-similarity:
	python src/visualization/cosine_similarity.py

# ==========================
# YAML Config Check
# ==========================
check-config:
	cat config/config.yaml

# ==========================
# Data Preprocessing
# ==========================
preprocess:
	python src/data_preprocessing/preprocess_jleague.py

# ==========================
# Aggregate Metrics
# ==========================
metrics:
	python src/metrics.py

# ==========================
# Run Sequence Analysis
# ==========================
run-sequence:
	python src/analysis/save_sequence.py
