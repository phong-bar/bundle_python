from bundle_cli import api

orders = """
#774104.2
#772467.2
#772115.2
#772117.2
#771422.2
#771286.2
#771288.2
#771634.2
#770324.2
#769624.2
#768728
#769395.2
#769351
#769035.2
#769477.2
#768043.2
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
