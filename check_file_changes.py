import os
import subprocess
import sys
import joblib

def get_changed_files():
    try:
        commit_range = f"{os.environ['GITHUB_EVENT_BEFORE']}..{os.environ['GITHUB_EVENT_AFTER']}"
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
    # Load models
    model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)
    
    num_files_changed_scaled = scaler.transform([[num_files_changed]])
    
    prediction = model.predict(num_files_changed_scaled)
    return "Anomaly" if prediction == -1 else "Normal"

def main():
    model_file = "isolation_forest_model.pkl"
    scaler_file = "scaler.pkl"

    changed_files = get_changed_files()

    result = test_entry(len(changed_files), model_file, scaler_file)

    print(f"Changed files: {changed_files}")
    if result == "Anomaly":
        print("Commit is NOT valid!")
        sys.exit(1)
    else:
        print("Commit is valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()

