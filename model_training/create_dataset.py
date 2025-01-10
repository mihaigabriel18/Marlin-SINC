import subprocess
import csv

def get_commit_history(repo_path):
    """
    Retrieves the commit history of a repository along with the number of files changed.
    """
    try:
        # Navigate to the repository path
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--pretty=format:%H", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout

        commits = []
        current_commit = None

        # Parse the output
        for line in output.splitlines():
            if line.strip() == "":  # New commit separator
                continue
            if len(line.strip()) == 40:  # Commit hash
                if current_commit:
                    commits.append(current_commit)
                current_commit = {"hash": line.strip(), "files": []}
            else:  # File change
                if current_commit:
                    current_commit["files"].append(line.strip())

        # Add the last commit
        if current_commit:
            commits.append(current_commit)

        # Add the number of files changed to each commit
        for commit in commits:
            commit["num_files_changed"] = len(commit["files"])

        return commits

    except subprocess.CalledProcessError as e:
        print(f"Error while running git command: {e}")
        return []

def save_to_csv(commits, output_file):
    """
    Saves the commit data to a CSV file.
    """
    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["hash", "num_files_changed"])
        writer.writeheader()
        for commit in commits:
            writer.writerow({
                "hash": commit["hash"],
                "num_files_changed": commit["num_files_changed"]
            })

def main():
    repo_path = "."
    output_file = "commit_history.csv"

    print("Fetching commit history...")
    commits = get_commit_history(repo_path)

    print(f"Saving {len(commits)} commits to {output_file}...")
    save_to_csv(commits, output_file)

    print("Dataset created successfully!")

if __name__ == "__main__":
    main()
