import os
from dotenv import load_dotenv
import oracledb

load_dotenv()

USERNAME = os.getenv('Username')
PASSWORD = os.getenv('Password')
HOSTNAME = os.getenv('Hostname')
PORT = os.getenv('Port')
SID = os.getenv('sid')

DSN = f"{HOSTNAME}:{PORT}/{SID}"

# Example: Query AAS2 for date mismatch
with oracledb.connect(user=USERNAME, password=PASSWORD, dsn=DSN) as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM AAS2 WHERE DATE_TABLE <> '08-08-2025'")
    count = cursor.fetchone()[0]
    print(f"AAS2 records with date mismatch: {count}")
    # Add more queries as needed for other test cases
    cursor.close()
