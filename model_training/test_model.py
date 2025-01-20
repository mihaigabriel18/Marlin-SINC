import joblib

def test_entry(num_files_changed, model_file, scaler_file):
    model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)
    
    num_files_changed_scaled = scaler.transform([[num_files_changed]])
    
    prediction = model.predict(num_files_changed_scaled)
    return "Anomaly" if prediction == -1 else "Normal"


if __name__ == "__main__":
    model_file = "isolation_forest_model.pkl"
    scaler_file = "scaler.pkl"
    
    num_files_changed = 100
    
    result = test_entry(num_files_changed, model_file, scaler_file)
    print(f"Commit with {num_files_changed} files changed is: {result}")
