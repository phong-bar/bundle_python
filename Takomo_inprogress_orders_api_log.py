from bundle_cli.api import Bundle
import time
import random

bundle = Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Takomo")
in_progress_orders = bundle.get_orders(status="in_progress", search="CB-HKOUT")
print(f"found {len(in_progress_orders.get('data'))} orders.")
count = 0
for order in in_progress_orders.get("data"):
    # print(order.get("uuid"), end=" ")
    print(order.get("source_identifier"), end=" ")
    bundle.order_uuid = order.get("uuid")
    api_logs = bundle.get_order_api_logs()
    print(api_logs[-1]["created_at"], end=": ")
    if api_logs[-1]["title"] == "Order has been pushed to Kerry Takomo.":
        print("\r", end="")

    else:
        print(api_logs[-1]["title"])
        count += 1
    time.sleep(random.uniform(0.5, 1.5))
print(f"---\nTotal orders with problems according to API logs: {count}")