from setuptools import setup, find_packages

setup(
    name="football_project",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "statsbombpy",
        "scikit-learn",
        "pyyaml",
        "tqdm",
        "jupyter"
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "run-preprocessing=src.data_processing.preprocess_jleague:main",
            "run-metrics=src.feature_engineering.metrics:main",
            "run-visualization=src.visualization.pca_cluster:main"
        ]
    },
    author="Aritra Majumdar",
    description="An end-to-end football analytics project",
    license="MIT",
    url="https://github.com/kaii55/Football_project"
)

