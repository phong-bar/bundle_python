import os
import requests
from dotenv import load_dotenv
from typing import Optional


class WooCommerce:
    def __init__(
        self,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        base_url: str = "https://www.thehandy.com/wp-json/wc/v3/orders",
        tracking_url: str = "https://www.thehandy.com/wp-json/wc-shipment-tracking/v3/orders",
    ):
        if consumer_key is None or consumer_secret is None:
            load_dotenv()
            consumer_key = consumer_key or os.getenv("WOOCOMMERCE_CONSUMER_KEY")
            consumer_secret = consumer_secret or os.getenv("WOOCOMMERCE_CONSUMER_SECRET")

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_url = base_url
        self.tracking_url = tracking_url
        self.auth = (consumer_key, consumer_secret)
        self.session = requests.Session()

    def upload_tracking(self, order_id: str, tracking_provider: str, tracking_link: str, tracking_number: str):
        upload_response = self.session.request(
            method="POST",
            url=f"{self.tracking_url}/{order_id}/shipment-trackings",
            json={
                "tracking_provider": tracking_provider,
                "custom_tracking_link": tracking_link,
                "tracking_number": tracking_number,
            },
            auth=self.auth,
        )
        upload_response.raise_for_status()
        return upload_response.json()

    def mark_order_completed(self, order_id: str):
        mark_completed_response = self.session.request(
            method="PUT",
            url=f"{self.base_url}/{order_id}/",
            json={"status": "completed"},
            auth=self.auth,
        )
        mark_completed_response.raise_for_status()
        return mark_completed_response.json()
