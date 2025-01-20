import subprocess
import csv

def get_commit_history(repo_path):

    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--pretty=format:%H", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout

        commits = []
        current_commit = None

        for line in output.splitlines():
            if line.strip() == "":
                continue
            if len(line.strip()) == 40:
                if current_commit:
                    commits.append(current_commit)
                current_commit = {"hash": line.strip(), "files": []}
            else:
                if current_commit:
                    current_commit["files"].append(line.strip())

        if current_commit:
            commits.append(current_commit)

        for commit in commits:
            commit["num_files_changed"] = len(commit["files"])

        return commits

    except subprocess.CalledProcessError as e:
        print(f"Error while running git command: {e}")
        return []

def save_to_csv(commits, output_file):
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
