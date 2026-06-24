from bundle_cli import api

bundle = api.Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Ohdoki")
bundle.select_order(order_reference="BL16Z0OQD")

response = bundle.update_order_details(currency="USD")

response.raise_for_status()
result = response.json()

print(f"Order {bundle.order_uuid} - currency updated to {result['data']['currency']}")

