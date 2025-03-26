import argparse
import pandas as pd
import os
from src.data_loader import get_historical_data
from src.anomaly_detection import train_model, predict_anomaly
from src.anomaly_classification import anomaly_classification
from src.config import DATA_DIR, anomaly_prediction_dataset, model_path, rule_based_classified_anomalies, anomalies_with_insights
from src.generate_insight import generate_insight

def main():
    # Load or generate historical data
    # print("yaha aaya")
    dataset = get_historical_data()
    # print(dataset)
    model, features = train_model(dataset)
    
    prediction_dataset, anomaly_df = predict_anomaly(dataset, model, features)
    anomaly_df.to_csv(anomaly_prediction_dataset, index=False)
    
    classified_anomaly_df = anomaly_classification(anomaly_df)
    classified_anomaly_df.to_csv(rule_based_classified_anomalies, index=False)
    
    # Generate insights
    
    insight_summary = generate_insight(classified_anomaly_df)
    insight_summary.to_csv(anomalies_with_insights, index=False)
    
    


if __name__ == "__main__":
    main()