from bundle_cli.api import Bundle

bundle = Bundle()

bundle.login()
bundle.select_client(search_for_client_name="Blueprint")

orders = ['673566']
for order in orders:
    bundle.select_order(order_reference=order)
    bundle.update_order_status('cancelled')