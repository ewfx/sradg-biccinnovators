import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from src.config import anomaly_prediction_dataset, model_path

def train_model(dataset):
    
    # Create a derived feature: Deviation (%) based on Balance Difference and GL Balance
    dataset["Deviation (%)"] = (dataset["Balance Difference"] / dataset["GL Balance"]) * 100
    
    # Define the features for training the model
    features = ["GL Balance", "IHub Balance", "Balance Difference", "Deviation (%)"]
    
    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(dataset[features])
    
    joblib.dump(model, model_path)
    
    return model, features


def predict_anomaly(dataset, model, features = None):
    
    if features is None:
        features = ["GL Balance", "IHub Balance", "Balance Difference", "Deviation (%)"]
    
    # Predict anomalies on the historical dataset
    predictions = model.predict(dataset[features])
    
    # IsolationForest returns -1 for anomalies and 1 for normal instances.
    dataset["Anomaly_Prediction"] = ["Anomaly" if pred == -1 else "Normal" for pred in predictions]
    
    dataset["Anomaly_Score"] = model.decision_function(dataset[features])
    
    # Filter only the rows predicted as anomalies
    anomaly_df = dataset[dataset["Anomaly_Prediction"] == "Anomaly"]
    
    # anomaly_df.to_csv(anomaly_prediction_dataset, index=False)
    
    return dataset, anomaly_df