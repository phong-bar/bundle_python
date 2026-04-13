from bundle_cli import api

orders = """
CB-USOUT142133
CB-USOUT143701
CB-USOUT144145
CB-USOUT144103
CB-USOUT144100
CB-USOUT143958
CB-USOUT144077
CB-USOUT143728
CB-USOUT144251
CB-USOUT144416
CB-USOUT144255
CB-USOUT144245
CB-USOUT144274
CB-USOUT144278
CB-USOUT144467
CB-USOUT144322
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

