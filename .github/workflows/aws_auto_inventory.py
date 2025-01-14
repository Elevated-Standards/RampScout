import os
import subprocess
import sys
from datetime import datetime

# Constants
AWS_REGION = "us-east-1"  # Hardcoded region for testing
CI_COMMIT_MESSAGE_FETCH = "Fetched AWS Assets"
CI_COMMIT_MESSAGE_PROCESS = "Processed FedRAMP AWS Inventory"
GITHUB_USER = "GitHub Actions"
GITHUB_EMAIL = "actions@github.com"
REPO_URL = "https://github.com/aws-samples/aws-auto-inventory.git"
CONFIG_PATH = "../config/aws.json"
ENABLE_COMMIT_AND_PUSH = false  # Toggle to enable/disable committing and pushing results

# Utility functions
def run_command(command, env=None):
    """Runs a shell command."""
    result = subprocess.run(command, shell=True, env=env, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        print(result.stderr)
        sys.exit(1)
    return result.stdout.strip()

def configure_aws_cli():
    """Configures AWS CLI using environment variables."""
    print("Configuring AWS CLI...")
    aws_access_key = os.getenv("AUTOMATION_AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AUTOMATION_AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key or not AWS_REGION:
        print("AWS credentials or region are not set.", file=sys.stderr)
        sys.exit(1)

    run_command(f"aws configure set aws_access_key_id {aws_access_key}")
    run_command(f"aws configure set aws_secret_access_key {aws_secret_key}")
    run_command(f"aws configure set region {AWS_REGION}")

    # Verify credentials
    print("Verifying AWS credentials...")
    run_command("aws sts get-caller-identity")

def clone_and_run_inventory_scan():
    """Clones the AWS Auto Inventory repo and runs the inventory scan."""
    print("Cloning AWS Auto Inventory repository...")
    run_command(f"git clone {REPO_URL}")
    os.chdir("aws-auto-inventory")
    run_command("pip install -r requirements.txt")

    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M")
    output_dir = f"../data/json/aws/{timestamp}/{AWS_REGION}"
    os.makedirs(output_dir, exist_ok=True)

    print("Running AWS inventory scan...")
    run_command(f"python3 scan.py -s {CONFIG_PATH} -r {AWS_REGION} --output_dir {output_dir}")
    os.chdir("..")

def commit_and_push_results(commit_message, folder):
    """Commits and pushes the results to the repository."""
    if not ENABLE_COMMIT_AND_PUSH:
        print(f"Skipping commit and push for {folder}.")
        return

    print(f"Committing and pushing results from {folder}...")
    run_command("git config --local user.name \"{}\"".format(GITHUB_USER))
    run_command("git config --local user.email \"{}\"".format(GITHUB_EMAIL))
    run_command(f"mkdir -p {folder}")
    run_command(f"git add {folder}")
    try:
        run_command(f"git commit -m \"{commit_message}\"")
    except Exception as e:
        print(f"No changes to commit: {e}")
    run_command("git push origin HEAD")

def process_inventory():
    """Processes the inventory data."""
    print("Processing inventory data...")
    run_command("python3 main.py")

# Main script
if __name__ == "__main__":
    # Step 1: Configure AWS CLI
    configure_aws_cli()

    # Step 2: Clone and run inventory scan
    clone_and_run_inventory_scan()

    # Step 3: Commit and push fetched assets
    commit_and_push_results(CI_COMMIT_MESSAGE_FETCH, "data/json/aws")

    # Step 4: Process inventory data
    process_inventory()

    # Step 5: Commit and push processed results
    commit_and_push_results(CI_COMMIT_MESSAGE_PROCESS, "output")
