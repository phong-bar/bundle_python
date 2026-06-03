from bundle_cli import api

orders = """
#747217.2
#747217.2
#748024.2
#748024.2
#748085.2
#748295.2
#747986.2
#749346.2
#749346.2
#749002.2
#749002.2
#750573.2
#752360
#752360
#753549
#753549
#752948.2
#752948.2
#752948.2
#752953.2
#752953.2
LLELNAL3N
"""
status = "created"

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Blueprint")

order_list = [line.strip() for line in orders.split(sep="\n")]
for order in order_list:
    if order != "":
        bundle.select_order(order_reference=order)
        order_status = bundle.update_order_status(status=status)
        print(f"{order} - {order_status['data']['status']}")

