from bundle_cli import api

orders = """
FA-EU-7527
FA-EU-7462
FA-EU-6883
FA-EU-6884
FA-EU-6881
FA-EU-6880
FA-EU-7759
FA-EU-8050
"""
status = "cancelled"

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Freak")

order_list = [line.strip() for line in orders.split(sep="\n")]
for order in order_list:
    if order != "":
        bundle.select_order(order_reference=order)
        order_status = bundle.update_order_status(status=status)
        print(f"{order} - {order_status['data']['status']}")

