import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib


def train_and_save_model(input_csv, model_file, scaler_file):
    data = pd.read_csv(input_csv)
    
    scaler = StandardScaler()
    X = scaler.fit_transform(data[["num_files_changed"]])
    
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    
    joblib.dump(model, model_file)
    joblib.dump(scaler, scaler_file)
    
    print(f"Model saved to {model_file}")
    print(f"Scaler saved to {scaler_file}")


if __name__ == "__main__":
    input_csv = "commit_history.csv"
    model_file = "isolation_forest_model.pkl"
    scaler_file = "scaler.pkl"
    
    train_and_save_model(input_csv, model_file, scaler_file)
