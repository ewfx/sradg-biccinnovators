import os


# Base directory: adjust as needed
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

dataset_path = os.path.join(DATA_DIR, "historical_anomaly_dataset.csv")

anomaly_prediction_dataset = os.path.join(DATA_DIR, "prediction_anomaly_dataset.csv")

model_path = os.path.join(DATA_DIR, "model.pkl")

rule_based_classified_anomalies = os.path.join(DATA_DIR, "classified_anomalies.csv")

anomalies_with_insights = os.path.join(DATA_DIR, "anomalies_with_insights.csv")