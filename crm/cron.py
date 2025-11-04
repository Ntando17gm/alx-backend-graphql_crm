import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"

def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes and optionally checks GraphQL hello."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # Log to file (append mode)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

    # GraphQL check (optional)
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)
    query = gql("{ hello }")

    try:
        client.execute(query)
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} GraphQL hello OK\n")
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} GraphQL check failed: {e}\n")
