from bundle_cli import api
from datetime import date, timedelta
from time import sleep

bundle = api.Bundle()
bundle.login()

# loop through all clients

clients = bundle.get_clients()
ignore_list = [
    "93c23567-3fd8-4ef3-a71a-7dddfe17336e", # freak athelete
    "f854f54e-407d-4d67-9e58-6259adcefce8", # grunovis
    "84aee3d7-d888-4f76-9467-7a4b915975c6", # test
    "69e5323f-649a-4059-a959-735d233eba3a", # test
    "6de3718a-74f2-46fb-810e-498aa3f7201e", # miller harris
    "8486847d-1ae6-4737-839b-0bb139d44e1f", # test
    "6cd38d10-5620-4ab7-9ef8-71b20aabecac", # test
    "6ab1b128-81b4-46e4-97a0-5ff51d81858d", # wooting
]
start_date = date.today() - timedelta(days=180)
end_date = date.today() - timedelta(days=1)  # Check orders from the last 30 days

for client in clients.get('data', []):
    if client.get('uuid') in ignore_list:
        print(f"Skipping client: {client.get('name')} (ID: {client.get('uuid')})")
    else:
        client_id = client.get('uuid')
        client_name = client.get('name')
        print(f"Checking orders for client: {client_name} (ID: {client_id})", end="\t")
        bundle.select_client(client_uuid = client_id)

        # Get orders for the client
        orders = bundle.get_orders(status='created', per_page=1000, start_date=start_date, end_date=end_date)
        if orders.get('meta').get('totalItems') == 0:
            print(f"No stuck orders found.")
        else:
            print(f"Found {orders.get('meta').get('totalItems')} stuck orders.")
            for order in orders.get('data', []):
                order_id = order.get('uuid')
                order_ref = order.get('source_identifier')
                if order_ref[0:5] == "CB-US":
                    print(f"Skipping order {order_ref} as it is a CB-US order.")
                    continue
                else:
                    order_date = order.get('created_at')
                    bundle.select_order(order_uuid=order_id)
                    api_logs = bundle.get_order_api_logs()
                    print(f"https://admin.bundle.wayfindr.io/clients/{client_id}/orders/{order_id}")
                    print(f"Order ID:\t{order_id}\nReference:\t{order_ref}\nCreated At:\t{order_date}")
                    if len(api_logs) <= 1:
                        print(f"Only {len(api_logs)} log entries found for Order ID {order_id}.")
                    else:
                        print(f"API Logs:\t[{api_logs[-1].get('status_code')}] {api_logs[-1].get('title')}\n{api_logs[-1].get('body_response') if len(api_logs[-1].get('body_response')) < 300 else 'Redacted due to length'}")
                    sleep(5)
                print("-" * 70)
            print("=" * 70)
    print("\n")    # Check if the order is stuck (e.g., status is 'pending' for more than 7 days)
            