#!/usr/bin/env python3
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"

def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def main():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

    query = gql(f"""
    query {{
        orders(orderDate_Gte: "{seven_days_ago}") {{
            id
            customer {{
                email
            }}
        }}
    }}
    """)

    try:
        result = client.execute(query)
        orders = result.get("orders", [])
        if orders:
            for order in orders:
                order_id = order["id"]
                customer_email = order["customer"]["email"]
                log_message(f"Reminder for order {order_id} - Email: {customer_email}")
        else:
            log_message("No pending orders found.")

        print("Order reminders processed!")

    except Exception as e:
        log_message(f"Error fetching orders: {e}")

if __name__ == "__main__":
    main()


