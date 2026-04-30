from bundle_cli import api

orders = """
CB-USOUT142133
CB-USOUT143701
CB-USOUT144646
CB-USOUT145183
CB-USOUT145386
CB-USOUT144814
CB-USOUT144804
CB-USOUT146413
CB-HKOUT125672
CB-HKOUT125251
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

