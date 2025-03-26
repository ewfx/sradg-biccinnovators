import requests
import torch
import pandas as pd
from src.config import anomalies_with_insights
import json, re
from huggingface_hub import InferenceClient

# Replace with your Hugging Face API token
HF_API_TOKEN = "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"

# repo_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
repo_id = "mistralai/Mistral-7B-Instruct-v0.1"
# repo_id = "meta-llama/Meta-Llama-3-8B-Instruct"
# repo_id = "tiiuae/falcon-7b-instruct"

# Initialize LLM client with API token
llm_client = InferenceClient(
    model=repo_id,
    token=HF_API_TOKEN,  # Add authentication token
    timeout=120,
)

def generate_insights_for_anomaly(anomaly_details: dict) -> str:
    
    # Construct the prompt based on the anomaly details.
    prompt = (
        f"Analyze the following financial anomaly and provide insights into its potential causes and corrective actions:\n\n"
        f"Company: {anomaly_details.get('Company', 'N/A')}\n"
        f"Account: {anomaly_details.get('Account', 'N/A')}\n"
        f"Currency: {anomaly_details.get('Currency', 'N/A')}\n"
        f"GL Balance: {anomaly_details.get('GL Balance', 'N/A')}\n"
        f"IHub Balance: {anomaly_details.get('IHub Balance', 'N/A')}\n"
        f"Balance Difference: {anomaly_details.get('Balance Difference', 'N/A')}\n"
        f"Anomaly Classification: {anomaly_details.get('Rule_Based_Bucket_Name', 'Not Provided')}\n\n"
        "Provide only an analytical explanation of the root cause and potential corrective actions. Do not repeat the details."
    )

    try:
        response = llm_client.post(json={"inputs": prompt, "parameters": {"max_new_tokens": 200}})
        # return response  # Directly returning the generated text
        response_json = json.loads(response)  # Properly parse the JSON response
        generated_text = response_json[0]["generated_text"] if isinstance(response_json, list) else "No insights generated."
        
        # Extract only from "Root Cause" onwards
        match = re.search(r"Root Cause:.*", generated_text, re.DOTALL)
        return match.group(0).strip() if match else generated_text.strip()

    except Exception as e:
        return f"Error generating insights: {e}"
    

def generate_insight(classified_anomaly_df):
    
    insights_list = []
    
        # Iterate over each anomaly row and generate insights
    for idx, row in classified_anomaly_df.iterrows():
        anomaly_details = {
            "Company": row.get("Company", "N/A"),
            "Account": row.get("Account", "N/A"),
            "Currency": row.get("Currency", "N/A"),
            "GL Balance": row.get("GL Balance", "N/A"),
            "IHub Balance": row.get("IHub Balance", "N/A"),
            "Balance Difference": row.get("Balance Difference", "N/A"),
            "Rule_Based_Bucket_Name": row.get("Rule_Based_Bucket_Name", "Not Provided")
        }
        
        try:
            insight = generate_insights_for_anomaly(anomaly_details)
        except Exception as e:
            insight = f"Error generating insights: {e}"
        
        insights_list.append(insight)
        # print(f"Processed row {idx+1}/{len(classified_anomaly_df)}")
        
    # Add the generated insights as a new column
    classified_anomaly_df["Insights"] = insights_list
    
    # Save the enriched dataset to CSV
    # classified_anomaly_df.to_csv(anomalies_with_insights, index=False)
    # print(f"Generated insights saved to '{anomalies_with_insights}'")
    
    return classified_anomaly_df
    
    