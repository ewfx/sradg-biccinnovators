import pandas as pd
import random

def generate_historical_data(num_samples=1000, anomaly_ratio=0.4):
    """
    Generates synthetic historical data with a given anomaly ratio and saves it as a CSV.
        
    The generated dataset includes the following columns:
      - As of Date, Company, Account, AU, Currency, Primary Account, Secondary Account,
      - GL Balance, IHub Balance, Balance Difference, Match Status, Comments
    """
    
    data = []
    
    for i in range(num_samples):
        # Random date (month/day/year format)
        as_of_date = f"{random.randint(1, 12)}/30/2024"
        
        # Randomly choose values for the categorical columns
        company = random.choice(["00000", "00001", "00002", "00003"])
        account = random.choice(["1619205", "1619288", "1618001", "1623456"])
        au = random.randint(4000, 7000)
        currency = random.choice(["USD", "EUR", "GBP", "INR"])
        primary_account = random.choice(["ALL OTHER LOANS", "MORTGAGES", "CREDIT CARDS"])
        secondary_account = random.choice(["DEFERRED COSTS", "DEFERRED ORIGINATION FEES", "PRINCIPAL", "INTEREST INCOME"])
        
        # Generate GL Balance within a specified range
        gl_balance = random.randint(10000, 100000)
        
        if i < num_samples * (1 - anomaly_ratio):
            # Normal cases: IHub Balance is close to GL Balance (within ±1 USD variation)
            ihub_balance = gl_balance + random.uniform(-1, 1)
            match_status = "Match"
            balance_diff = ihub_balance - gl_balance
            comments = "Difference is within tolerance (less than 1 USD)"
        else:
            # Anomalous cases: Introduce significant imbalance
            ihub_balance = gl_balance + random.choice([-50000, 50000, -20000, 20000])
            match_status = "Break"
            balance_diff = ihub_balance - gl_balance
            comments = "Significant balance discrepancy"
        
        data.append([
            as_of_date, company, account, au, currency,
            primary_account, secondary_account,
            gl_balance, ihub_balance, balance_diff,
            match_status, comments
        ])
    
    # Create a DataFrame from the generated data
    df = pd.DataFrame(data, columns=[
        "As of Date", "Company", "Account", "AU", "Currency", 
        "Primary Account", "Secondary Account", "GL Balance",
        "IHub Balance", "Balance Difference", "Match Status", "Comments"
    ])
    
    # Save the DataFrame to a CSV file
    # df.to_csv(output_file, index=False)
    print(f"Historical dataset with {anomaly_ratio*100}% anomalies generated and saved")
    
    return df


