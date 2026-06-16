"""
Get the tracking data from Bundle, then upload to WooCommerce for Ohdoki
"""

from bundle_cli import api
from bundle_cli.additional_api import WooCommerce
import time

Bundle = api.Bundle()
Bundle.login()
Bundle.select_client(search_for_client_name="Ohdoki")

Woo = WooCommerce()

orders = """
363730
363726
363725
363724
363720
363719
363715
363714
363712
363711
363710
363698
363692
363689
363686
363685
363683
363682
363676
363672
363664
363663
363661
363659
363657
363655
363654
363649
363648
363645
363644
363642
363641
363637
363634
363633
363625
363624
363622
363620
363619
363617
363611
363608
363605
363603
363602
363601
363599
363597
363596
363591
363590
363587
363585
363584
363581
363579
363577
363573
363571
363567
363559
363547
363545
363544
363541
363505
363485
363459
363229
363032
362940
"""

for order in orders.strip().split("\n"):
    Bundle.select_order(order_reference=order)
    tracking = Bundle.get_order_details().get("data").get("shipments")[0]
    if tracking:
        print(f"{order}: {tracking}")
        Woo.upload_tracking(
            order_id=order,
            tracking_provider=tracking.get("courier_company"),
            tracking_link=tracking.get("courier_tracking_url"),
            tracking_number=tracking.get("courier_tracking_number"),
        )
        print(f"{order}: Tracking data uploaded successfully")
        Woo.mark_order_completed(order_id=order)
        print(f"{order}: Marked as completed on WooCommerce")
    else:
        print(f"{order}: No tracking data")
    time.sleep(1)

    

