from src.config import rule_based_classified_anomalies


# Predefined anomaly buckets mapping
ANOMALY_BUCKETS = {
    1: "Inconsistent variations in outstanding balances",
    2: "Consistent increase or decrease in outstanding balances",
    3: "Huge spike in outstanding balances",
    4: "Outstanding balances are not in line with previous months",
    5: "Gradual deviation beyond threshold over multiple periods",
    6: "Sudden drop in outstanding balances",
    7: "High volatility in account balances over time",
    8: "Reversal or correction entry detected",
    9: "New account or currency not seen in historical data",  
    10: "Large single-month fluctuation with no prior history",
    11: "No clear pattern, but deviation exceeds threshold"
}


def anomaly_mapping(row):
    try:
        deviation = abs(row["Balance Difference"]) / row["GL Balance"] * 100
    except ZeroDivisionError:
        return 11
    
    if deviation < 5:
        return 11
    elif 5 <= deviation < 10:
        return 1
    elif 10 <= deviation < 15:
        return 2
    elif 15 <= deviation < 25:
        if row["Balance Difference"] > 0:
            return 3
        else:
            return 6
    elif deviation >= 25:
        if row["Balance Difference"] > 0:
            return 10
        else:
            return 8
    else:
        return 11
    

def anomaly_classification(anomaly_df):
    
    # Apply the rule-based classification to each row
    anomaly_df["Rule_Based_Bucket"] = anomaly_df.apply(anomaly_mapping, axis=1)
    
    anomaly_df["Rule_Based_Bucket_Name"] = anomaly_df["Rule_Based_Bucket"].map(ANOMALY_BUCKETS)
    
    anomaly_df.drop(columns=["Rule_Based_Bucket"], inplace=True)
    
    # anomaly_df.to_csv(rule_based_classified_anomalies, index=False)
    # print(f"Rule-based anomaly classification complete. Output saved to '{rule_based_classified_anomalies}'")
    
    return anomaly_df
