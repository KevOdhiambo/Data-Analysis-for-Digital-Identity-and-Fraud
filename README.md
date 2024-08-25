# E-commerce Analysis Project

This project analyzes digital identity verification and fraud patterns in e-commerce transactions.

## Project Structure

- `data/`: Contains the generated dataset and SQLite database
- `src/`: Python scripts for data generation, import, analysis, and visualization
- `sql/`: SQL queries for analysis
- `notebooks/`: Jupyter notebooks for exploratory analysis
- `outputs/`: Figures and reports generated from the analysis

## Setup and Running the Project

1. Install the required packages:
`pip install -r requirements.txt`
2. Generate the dataset:
`python src/data_generation.py`

3. Import data to SQLite:
`python src/data_import.py`
 
4. Run SQL analysis:
`python src/sql_analysis.py`
 
5. Perform machine learning analysis:
`python src/ml_analysis.py`
 
6. Generate visualizations:
`python src/visualizations.py`

7. Generate report based on analsyis
`python src/generate_report.py`
 
All outputs will be saved in the `outputs/` directory.

8. ## Running the Entire Project

To run the entire analysis pipeline, including data generation, analysis, and report generation, use the following command:
`python run_analysis.py`

## Exploratory Analysis

For interactive exploratory analysis, open the Jupyter notebook:
jupyter notebook notebooks/exploratory_analysis.ipynb
 
