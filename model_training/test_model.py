import joblib

def test_entry(num_files_changed, model_file, scaler_file):
    """
    Test if a given entry is an anomaly using a pre-trained Isolation Forest model.
    
    Args:
    - num_files_changed (int): The number of files changed in the commit.
    - model_file (str): Path to the saved Isolation Forest model file.
    - scaler_file (str): Path to the saved scaler file.
    
    Returns:
    - str: "Anomaly" if the entry is an anomaly, "Normal" otherwise.
    """
    # Load the saved model and scaler
    model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)
    
    # Preprocess the input
    num_files_changed_scaled = scaler.transform([[num_files_changed]])
    
    # Predict anomaly or normal
    prediction = model.predict(num_files_changed_scaled)
    return "Anomaly" if prediction == -1 else "Normal"


if __name__ == "__main__":
    # File paths
    model_file = "isolation_forest_model.pkl"  # Path to the saved model
    scaler_file = "scaler.pkl"  # Path to the saved scaler
    
    # Example input
    num_files_changed = 100  # Replace with the number of files changed to test
    
    # Test if the entry is an anomaly
    result = test_entry(num_files_changed, model_file, scaler_file)
    print(f"Commit with {num_files_changed} files changed is: {result}")
