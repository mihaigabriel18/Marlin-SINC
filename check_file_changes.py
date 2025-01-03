import os
import subprocess
import sys
import joblib

def get_changed_files():
    try:
        # Get the commit range from environment variables
        commit_range = f"{os.environ['GITHUB_EVENT_BEFORE']}..{os.environ['GITHUB_EVENT_AFTER']}"
        # Run git diff to get the list of changed files
        result = subprocess.run(
            ["git", "diff", "--name-only", commit_range],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.splitlines()
        return files
    except Exception as e:
        print(f"Error determining changed files: {e}")
        return []

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

def main():
    model_file = "isolation_forest_model.pkl"  # Path to the saved model
    scaler_file = "scaler.pkl"  # Path to the saved scaler

    changed_files = get_changed_files()

    result = test_entry(len(changed_files), model_file, scaler_file)

    print(f"Changed files: {changed_files}")
    if result == "Anomaly" > 1:
        print("Commit is NOT valid!")
        sys.exit(1)  # Exit with a non-zero code to fail the workflow
    else:
        print("Commit is valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()

