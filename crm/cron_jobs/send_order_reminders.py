#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# GraphQL query to get orders within the last 7 days
query = """
query {
  orders {
    id
    customerEmail
    orderDate
  }
}
"""

def log_message(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def main():
    try:
        # Make the GraphQL request
        response = requests.post(GRAPHQL_ENDPOINT, json={"query": query})
        response.raise_for_status()
        data = response.json()

        # Extract and filter orders
        orders = data.get("data", {}).get("orders", [])
        week_ago = datetime.now() - timedelta(days=7)
        recent_orders = [
            order for order in orders
            if order.get("orderDate") and datetime.fromisoformat(order["orderDate"]) >= week_ago
        ]

        # Log each order reminder
        if recent_orders:
            for order in recent_orders:
                log_message(f"Reminder: Order {order['id']} - Customer {order['customerEmail']}")
        else:
            log_message("No recent orders found.")

        print("Order reminders processed!")

    except Exception as e:
        log_message(f"Error fetching orders: {e}")

if __name__ == "__main__":
    main()

