import pandas as pd

def detect_anomalies(df: pd.DataFrame):
    anomalies = []

    #make sure there are mandatory columns in the csv file.
    required_columns = ["transaction_id", "card_id", "amount", "timestamp"]
    if not all(col in df.columns for col in required_columns):
        return [{"error": f"Missing required columns: {required_columns}"}]

    #convert the timestamp col to time.
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by=['card_id', 'timestamp'])
    df["time_diff"] = df.groupby('card_id')["timestamp"].diff()

    #rule 1: high amount
    high_amounts = df[df["amount"] > 5000]
    high_amounts['reason'] = "High amount"

    #rule 2: transactions in the same card less than 5 minutes.
    quick_succession = df[df["time_diff"] < pd.Timedelta(minutes=5)]
    quick_succession['reason'] = "Quick succession transaction"

    #rule 3:

    #convert time_diff from seconds to minutes.
    for frame in [high_amounts, quick_succession]:
        frame['time_diff_minutes'] = frame['time_diff'].dt.total_seconds() // 60
        frame['time_diff_minutes'] = frame['time_diff_minutes'].fillna("N/A")

    #add reason why the transaction marked as anomalies.
    combined = pd.concat([high_amounts, quick_succession], ignore_index=True)
    selected_columns = ['transaction_id', 'card_id', 'amount', 'timestamp', 'time_diff_minutes', 'reason']

    return combined[selected_columns].to_dict(orient="records")