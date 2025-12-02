# crm/tasks.py

import datetime
import requests
from celery import shared_task

@shared_task
def generate_crm_report():
    url = "http://localhost:8001/graphql"

    query = """
    {
      customers {
        id
      }
      orders {
        id
        totalAmount
      }
    }
    """

    log_file = "/tmp/crm_report_log.txt"

    try:
        response = requests.post(url, json={"query": query})
        response.raise_for_status()
        data = response.json()

        customers = len(data["data"].get("customers", []))
        orders = data["data"].get("orders", [])

        total_orders = len(orders)
        total_revenue = sum(order.get("totalAmount", 0) for order in orders)

        line = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Report: {customers} customers, {total_orders} orders, {total_revenue} revenue\n"

        with open(log_file, "a") as f:
            f.write(line)

    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{datetime.datetime.now()} - Error: {str(e)}\n")

