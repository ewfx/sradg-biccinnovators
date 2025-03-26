from flask import Flask, render_template, Response, request, redirect
import pandas as pd
from src.config import model_path
import joblib, os
from src.anomaly_detection import train_model, predict_anomaly
from src.anomaly_classification import anomaly_classification
from src.generate_insight import generate_insight
from src.config import anomalies_with_insights
from main import main

# load model
model = joblib.load(model_path)

upload_fodler = "data/upload"
if not os.path.exists(upload_fodler):
    os.makedirs(upload_fodler)

app=Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == "POST":
        main()
    return render_template('index.html')


@app.route('/anomalies_report', methods=['GET', 'POST'])
def anomalies_report():
    df = pd.read_csv(anomalies_with_insights)
    # Convert DataFrame to HTML table
    predictions_df = df.to_html(classes="table table-striped", index=False)
    
    
    return render_template('anomalies_report.html', predictions_df=predictions_df)


@app.route('/anomaly_detection', methods=['GET', 'POST'])
def anomaly_detection():
    
    if request.method == "POST":
        file = request.files['file']
        if file and file.filename.endswith(".csv"):
            filepath = os.path.join(upload_fodler, file.filename)
            file.save(filepath)
            
            df = pd.read_csv(filepath)
            # print(df)
            df["Deviation (%)"] = (df["Balance Difference"] / df["GL Balance"]) * 100
            
            prediction, anomly_df = predict_anomaly(df, model)
            
            classified_anomaly_df = anomaly_classification(anomly_df)
            
            insight_summary = generate_insight(classified_anomaly_df)
                
            # print(insight_summary)
            insight_summary_df = insight_summary[['Account', 'GL Balance', 'IHub Balance', 'Balance Difference', 'Anomaly_Prediction', 'Rule_Based_Bucket_Name', 'Insights']]
            
            # Convert DataFrame to HTML table
            predictions_df = insight_summary_df.to_html(classes="table table-striped", index=False)

            return render_template('anomaly_detection.html', predictions_df=predictions_df)
        
    return render_template('anomaly_detection.html')


@app.route('/detection', methods=['GET', 'POST'])
def detection():
    
    if request.method == 'POST':
        try:
            asofdate = request.form['date']
            glbalance = int(request.form['glbalance'])
            ihubbalance = float(request.form['ihubbalance'])
            balancedifference = float(request.form['balancedifference'])
            company = int(request.form['company'])
            account = int(request.form['account'])
            au = int(request.form['au'])
            currency = request.form['currency']
            paccount = request.form['paccount']
            saccount = request.form['saccount']
            
            Deviation = (balancedifference/glbalance)*100 if glbalance != 0 else 0
            
            # Create a dictionary for DataFrame with the specified column order
            data = {
                "As of Date": [asofdate],
                "Company": [company],
                "Account": [account],
                "AU": [au],
                "Currency": [currency],
                "Primary Account": [paccount],
                "Secondary Account": [saccount],
                "GL Balance": [glbalance],
                "IHub Balance": [ihubbalance],
                "Balance Difference": [balancedifference],
                "Deviation (%)": [Deviation]
            }

            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            prediction, anomly_df = predict_anomaly(df, model)
            
            classified_anomaly_df = anomaly_classification(prediction)
            
            insight_summary = generate_insight(classified_anomaly_df)
                
            # print(insight_summary)
            
            # Convert DataFrame to HTML table
            predictions_df = insight_summary.to_html(classes="table table-striped", index=False)
            
            return render_template('detection.html', predictions_df=predictions_df) 
                
        except Exception as e:
            error = {"error": e}
            return render_template('detection.html')
        
        return render_template('detection.html')
        
    else:
        return render_template('detection.html')




if __name__=="__main__":
    app.run(debug=True)