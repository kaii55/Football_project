# ⚽ Football Project - J League Analysis

This project analyzes J League playing styles using StatsBomb Hudl data, performing data preprocessing, feature engineering, and advanced visualizations.

---

## 📂 Project Structure:
```
Football_project/
├── src/
│   ├── data_processing/         # Preprocess J League data
│   ├── feature_engineering/     # Compute football metrics (Possession, PPDA, Field Tilt, etc.)
│   ├── visualization/           # Perform PCA, KMeans clustering, and heatmaps
└── data/
    ├── raw/                    # Raw JSON files
    ├── processed/              # Processed data and results
    └── visualizations/         # Saved plots
```

---

## 💻 Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kaii55/Football_project.git
   cd Football_project
   ```

2. **Create a Virtual Environment:**
   ```bash
   conda create -n football_env python=3.9
   conda activate football_env
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃‍♂️ How to Run

### 1️⃣ **Step 1: Data Preprocessing**
```bash
python src/data_processing/preprocess_jleague.py
```
- **Input:** Raw JSON files (`sb_events.json`, `sb_matches.json`)
- **Output:** Processed `.parquet` file in `data/processed/`

### 2️⃣ **Step 2: Feature Engineering**
```bash
python src/feature_engineering/metrics.py
```
- Computes football metrics: Possession, PPDA, Field Tilt, Verticality, and more.
- **Output:** `jleague_metrics.xlsx` in `data/processed/`

### 3️⃣ **Step 3: Visualization & Analysis**
```bash
python src/visualization/pca_cluster.py
```
- **Visualizes:** PCA scatter plots, KMeans clusters, and cosine similarity heatmaps.
- **Output:** PNG files in `data/visualizations/`

---

## 📊 Outputs:
- Processed Data: `data/processed/`
- Visualizations: `data/visualizations/`

## ⚙️ Dependencies:
- Python 3.9  
- Pandas, NumPy, Matplotlib, Seaborn  
- Scikit-learn, mplsoccer  
- AdjustText  

## ✨ Author:
- **Aritra Majumdar**  
- Twitter: [@DataAnalyticEPL](https://twitter.com/DataAnalyticEPL)  

✅ **Run all steps at once (Optional):**
```bash
python src/data_processing/preprocess_jleague.py && \
python src/feature_engineering/metrics.py && \
python src/visualization/pca_cluster.py
```

## 📖 License:
This project is for educational purposes only.

