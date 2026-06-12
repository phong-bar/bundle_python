from bundle_cli import api

orders = """
#766382.2
#766785.2
#765561.2
#765423.2

#764117.2

#764201.2

#764324.2

#763653.2

#762358

#761492.2

#761657.2



#742816.2

#761073.2

#760548.2

#760592.2

#760795

#760515.2

#760625.2

#758913.2

#757843

#753994.2

#754799.2

#755038.2

#754417.2
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

