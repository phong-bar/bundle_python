from bundle_cli import api

orders = """
CB-USOUT144568
CB-USOUT144701
CB-USOUT144840
CB-USOUT144884
CB-USOUT145066
CB-USOUT144858
CB-USOUT144680
CB-USOUT144669
CB-USOUT144548
CB-USOUT145789
CB-USOUT145607
CB-USOUT145598
CB-USOUT145572
CB-USOUT145549
CB-USOUT145489
"""
status = "cancelled"

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Takomo")

order_list = [line.strip() for line in orders.split(sep="\n")]
for order in order_list:
    if order != "":
        bundle.select_order(order_reference=order)
        order_status = bundle.update_order_status(status=status)
        print(f"{order}: {order_status.get("data").get("status")}")

