from bundle_cli import api

orders = """
CB-EUOUT20647
CB-EUOUT20488
CB-EUOUT18787
CB-EUOUT17666
CB-EUOUT15432
CB-EUOUT13184
CB-EUOUT14158
CB-EUOUT15001
CB-EUOUT15114
CB-EUOUT21477
CB-USOUT158232
CB-USOUT157469
CB-USOUT157484
CB-USOUT161602
CB-EUOUT21587
CB-HKOUT133756
CB-USOUT162785
CB-USOUT162916
CB-USOUT162868
CB-USOUT51779
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

