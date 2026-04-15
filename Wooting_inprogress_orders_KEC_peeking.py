from bundle_cli.api import Bundle, OrderStatus
import requests
import time
import random

bundle = Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Wooting")  

in_progress_orders = bundle.get_orders(status="in_progress")
print(f"found {len(in_progress_orders.get("data"))} orders")
kerry = requests.Session()
kerry.headers.update({"Content-Type": "application/json"})
kerry_login = kerry.post(
    url=f"https://foms-api.kec-app.com/auth/login",
    json={
        "username": "keyboard.api",
        "password": "2B0iI6uZX5"
    }
)
kerry.headers.update({"Authorization": f"Bearer {kerry_login.json().get("token")}"})
print(kerry_login.json().get("token"))

for order in in_progress_orders.get("data"):
    order_number = order.get("source_identifier")
    print(order_number, end=" ")
    order_data_kerry = kerry.get(url=f"https://foms-api.kec-app.com/api/foms/v2/order/status",
    params={"orderNumber": order_number}
    )
    print(order_data_kerry.json().get("data").get("status"))
    time.sleep(random.uniform(1.5, 3.0))
