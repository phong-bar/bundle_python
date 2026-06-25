from bundle_cli.api import Bundle

bundle = Bundle()

bundle.login()
bundle.select_client(search_for_client_name="Blueprint")

orders = [
    "782470.2",
    "782746.2",
    "782121",
    "781597.2",
    "781714.2",
    "779365.2",
    "779316.2",
    "779405.2",
    "779810.2",
    "779579.2",
    "776568.2",
    "777163.2",
    "777240.2",
    "776704.2",
    "775640.2",
    "WGDEOORYW",
]
for order in orders:
    bundle.select_order(order_reference=order)
    result = bundle.update_order_status("created")
    print(f"{order} - {result['data']['status']}")
