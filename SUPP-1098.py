from bundle_cli import api

orders = """
43548

43524

43161

39311

39206

39099

38329

38264

38254

38239

38234

38166

38127

38117

38112

38092

38055

38050

38027

38026

38025

37987


29110
"""
status = "finalised"

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Uclips")

order_list = [line.strip() for line in orders.split(sep="\n")]
for order in order_list:
    if order != "":
        bundle.select_order(order_reference=order)
        order_status = bundle.update_order_status(status=status)
        print(f"{order} - {order_status['data']['status']}")
