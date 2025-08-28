import os
from dotenv import load_dotenv
import paramiko

load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_USER = os.getenv('SSH_USER')
SSH_KEY_PATH = os.getenv('SSH_KEY_PATH')
REMOTE_SCRIPT_PATH = os.getenv('REMOTE_SCRIPT_PATH')

# If key path is not set, fallback to password (not recommended for prod)
def get_ssh_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if SSH_KEY_PATH and os.path.exists(SSH_KEY_PATH):
        client.connect(SSH_HOST, username=SSH_USER, key_filename=SSH_KEY_PATH)
    else:
        # Prompt for password if key not available
        import getpass
        password = getpass.getpass(f"Password for {SSH_USER}@{SSH_HOST}: ")
        client.connect(SSH_HOST, username=SSH_USER, password=password)
    return client

def run_remote_script():
    client = get_ssh_client()
    stdin, stdout, stderr = client.exec_command(f"bash {REMOTE_SCRIPT_PATH}")
    output = stdout.read().decode()
    error = stderr.read().decode()
    client.close()
    return output, error

def parse_job_status(output):
    # Example: parse lines for 'Success' status
    statuses = [line for line in output.splitlines() if 'Success' in line]
    all_success = all('Success' in line for line in output.splitlines() if line.strip())
    return statuses, all_success

def main():
    print("Connecting to Unix server and running job status script...")
    output, error = run_remote_script()
    if error:
        print("Error running remote script:", error)
    print("Script Output:\n", output)
    statuses, all_success = parse_job_status(output)
    print("Job Statuses:", statuses)
    print("All jobs success:", all_success)
    return all_success

if __name__ == "__main__":
    main()
