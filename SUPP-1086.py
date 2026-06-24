from bundle_cli import api

orders = """
496105

463841

490543

465416

432262

433255

433252

431472
"""
status = "cancelled"

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Diggers Factory")

order_list = [line.strip() for line in orders.split(sep="\n")]
for order in order_list:
    if order != "":
        bundle.select_order(order_reference=order)
        order_status = bundle.update_order_status(status=status)
        print(f"{order} - {order_status['data']['status']}")
