import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib  # For saving/loading the model


def train_and_save_model(input_csv, model_file, scaler_file):
    """
    Train an Isolation Forest model on the `num_files_changed` feature and save it.
    """
    # Load the dataset
    data = pd.read_csv(input_csv)
    
    # Normalize the `num_files_changed` feature
    scaler = StandardScaler()
    X = scaler.fit_transform(data[["num_files_changed"]])
    
    # Train the Isolation Forest model
    model = IsolationForest(contamination=0.05, random_state=42)  # 5% anomalies
    model.fit(X)
    
    # Save the trained model and the scaler
    joblib.dump(model, model_file)
    joblib.dump(scaler, scaler_file)
    
    print(f"Model saved to {model_file}")
    print(f"Scaler saved to {scaler_file}")


if __name__ == "__main__":
    # File paths
    input_csv = "commit_history.csv"  # Input dataset
    model_file = "isolation_forest_model.pkl"  # Model file
    scaler_file = "scaler.pkl"  # Scaler file
    
    train_and_save_model(input_csv, model_file, scaler_file)
