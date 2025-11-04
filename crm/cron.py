import datetime
import requests

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # Log to file (append mode)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

    # Optionally, ping GraphQL hello field to check API responsiveness
    try:
        response = requests.post(GRAPHQL_ENDPOINT, json={"query": "{ hello }"})
        response.raise_for_status()
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} GraphQL check failed: {e}\n")
# Optionally ping GraphQL
# try:
#     response = requests.post(GRAPHQL_ENDPOINT, json={"query": "{ hello }"})
#     response.raise_for_status()
# except Exception as e:
#     with open(LOG_FILE, "a") as f:
#         f.write(f"{timestamp} GraphQL check failed: {e}\n")
