import requests
import datetime

# -------------------------------
#  Heartbeat Cron Job (Task 2)
# -------------------------------
def log_crm_heartbeat():
    log_file = "/tmp/crm_heartbeat_log.txt"
    with open(log_file, "a") as log:
        log.write(f"[{datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}] CRM is alive\n")

# -------------------------------
#  Low Stock Update Cron Job (Task 3)
# -------------------------------
def update_low_stock():
    url = "http://localhost:8001/graphql"
    query = """
    mutation {
      updateLowStockProducts {
        message
        updatedProducts {
          name
          stock
        }
      }
    }
    """

    log_file = "/tmp/low_stock_updates_log.txt"

    try:
        response = requests.post(url, json={"query": query})
        response.raise_for_status()
        data = response.json()

        with open(log_file, "a") as log:
            log.write(f"[{datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}] Mutation Response: {data}\n")

    except Exception as e:
        with open(log_file, "a") as log:
            log.write(f"[{datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}] Error: {str(e)}\n")



