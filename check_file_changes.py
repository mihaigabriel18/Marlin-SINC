import os
import subprocess
import sys

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

def main():
    changed_files = get_changed_files()
    print(f"Changed files: {changed_files}")
    if len(changed_files) > 1:
        print("More than one file changed!")
        sys.exit(1)  # Exit with a non-zero code to fail the workflow
    else:
        print("Commit is valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()
