from bundle_cli import api
import time


bundle = api.Bundle()

bundle.login()
bundle.select_client(search_for_client_name="Diggers Factory")

order_list = bundle.get_orders(per_page=300, status="finalised")["data"]
iter = 1
for order in order_list:
    print(f"[{iter:<3}/{len(order_list)}]", end=" ")
    print(f"Checking {order.get('uuid')}", end="... ")
    bundle.select_order(order.get("uuid"))
    time.sleep(1)
    api_logs = bundle.get_order_api_logs()
    time.sleep(1)
    ds_send_request_count = 0
    for log in api_logs:
        if log.get("title") == "Order has been pushed to Dealersend Diggers Factory" and log.get("status_code") == 200:
            ds_send_request_count += 1
    if ds_send_request_count > 1:
        print(f"pushed to Dealersend Diggers Factory {ds_send_request_count} times")
        print("\a")
    else:
        print("OK\n\033[K", end="")
    iter += 1
