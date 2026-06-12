from bundle_cli import api

orders = """
431817
423581
432083
431539
448272
448272
431638
431638
431820
423046
438645
469644
"""
status = "cancelled"

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Diggers")

order_list = [line.strip() for line in orders.split(sep="\n")]
for order in order_list:
    if order != "":
        bundle.select_order(order_reference=order)
        order_status = bundle.update_order_status(status=status)
        print(f"{order} - {order_status['data']['status']}")

