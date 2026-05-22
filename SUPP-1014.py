from bundle_cli import api

orders = """
GWADBZD1Z
#726721
#726683
#726490
#725919
#725910
#727611
#727559
#727591
#727706
#727137
#728808
#728732
#728862
ENEXJPWPO
#729633
#729656
#730388
#730488
#730548
#731268
#730704
#730714
#731309
#730917
#731359
#731802
#732304
#732007
#732118
#731900
#732611
#732581
#732678
#733722
#733210
#733018
#733915
#734882
#734403
#734775
#734221
#734738
#735304
#735984
#735936
#735532
#743009
#742960
#742963
#742968
#742959.2
#744256
#744832.2
#744907
#744545.2
#746188.2
#746120.2
#746247.2
#745959.2
#745862.2
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

