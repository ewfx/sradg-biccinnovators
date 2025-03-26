import os
import pandas as pd
from src.config import dataset_path
from src.data_generation import generate_historical_data

def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def get_historical_data(data_path = None):
    
    if data_path is None:
        data_path = dataset_path
        # print(data_path)
        
    if os.path.exists(data_path):
        historical_df = load_csv(data_path)
        print(f"Data loaded from '{data_path}'. shape: {historical_df.shape}")
        
    else:
        print("No valid data file provided. Generating synthetic data.")
        historical_df = generate_historical_data()
        # print(historical_df)
        historical_df.to_csv(data_path, index=False)
        print(f"Synthetic historical data generated and saved to '{data_path}'.")
        
    return historical_df