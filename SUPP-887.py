from bundle_cli import api

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Auteur B2B")
bundle.select_order(order_reference="AUT2436")

# print(bundle.get_order_details())
test_data = bundle.update_order_details()
print(test_data)
