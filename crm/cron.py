import requests
import datetime

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



