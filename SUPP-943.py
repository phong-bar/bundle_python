from bundle_cli import api

orders = """
CB-USOUT147516
CB-USOUT147382
CB-USOUT147355
CB-USOUT148216
CB-USOUT148294
CB-USOUT148206
CB-USOUT148192
CB-USOUT146542
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
        print(f"{order} - {order_status['data']['status']}")

