from bundle_cli.api import Bundle
import time
import random

bundle = Bundle()
bundle.login()
bundle.select_client(search_for_client_name="Uclips")

order_uuids = [
    "7fef1f80-e943-4ad7-ade0-68d520382737",
    "bf167666-032e-49f6-8297-9f66ccfbd3f3",
    "927e2330-7072-4c8b-8582-3baf33b6dc4b",
    "498c5533-0859-45c5-b893-bd0020f83eed",
    "f53e59f4-0455-4f35-8cdc-81036a0c33cc",
    "87e3499e-bbba-46a7-9a90-70f8cf8ffd76",
    "3f012288-5095-419d-8318-01b688bb17bf",
    "1fcb41db-4385-4a24-901d-c62b63cc8a21",
    "28ecab44-1823-41e0-bcea-0af24a815f9d",
    "4f1bfaa3-0c46-44b9-822a-eff5289caa2f",
    "4cd283c0-9891-444f-b2bb-ca1bbe40ddfd",
    "6e5eae36-2672-4088-b613-9cecb65646b6",
    "29cf7da4-9bad-41ec-9b8d-c2ec7ba24bb5",
    "32dbcbc5-3b34-4082-b938-c47002017710",
    "bacfb8fc-a5b1-4253-8ec9-adfd30308727",
    "a01dae4f-1ba9-4b51-b506-54f3f97eda79",
    "ec8d1c09-f71b-4e31-a8bc-8c3b80c90402",
    "b57b0701-ac5d-4ca0-9bed-c223afa117d9",
    "2b5373eb-7c5e-45e5-9d1e-ed769753d3fc",
    "f956895a-d151-4d19-9baa-02f04c940cce",
    "f27d3da1-1d29-4627-991f-3b8a1be4ee18",
    "248a4691-7766-4504-8c36-2ffb7b2e8f44",
    "d5c04e8f-3573-4aa6-adf0-bf202523ee54",
    "9f12bc06-61d0-4437-8c73-79b156723430",
]

results = []
for order_uuid in order_uuids:
    bundle.order_uuid = order_uuid
    api_logs = bundle.get_order_api_logs()
    if api_logs:
        latest_log = api_logs[-1]
        print(f"Order UUID: {order_uuid}")
        print(f"  Latest API Log: {latest_log['title']}")
        print(f"  Created At: {latest_log['created_at']}")
        print(f"  Method: {latest_log.get('method', 'N/A')}")
        print(f"  Path: {latest_log.get('path', 'N/A')}")
        print()
        results.append({
            "order_uuid": order_uuid,
            "title": latest_log.get("title", "N/A"),
            "created_at": latest_log.get("created_at", "N/A"),
            "method": latest_log.get("method", "N/A"),
            "path": latest_log.get("path", "N/A"),
        })
    else:
        print(f"Order UUID: {order_uuid}")
        print("  No API logs found.")
        print()
        results.append({
            "order_uuid": order_uuid,
            "title": "No API logs found",
            "created_at": "N/A",
            "method": "N/A",
            "path": "N/A",
        })
    time.sleep(random.uniform(0.5, 1.5))

# Save results to markdown file
with open("SUPP-1078.md", "w") as f:
    f.write("# SUPP-1078 - Uclips API Log Analysis\n\n")
    f.write("## Client: Uclips\n\n")
    f.write("| Order UUID | Latest API Log | Created At | Method | Path |\n")
    f.write("|------------|---------------|------------|--------|------|\n")
    for r in results:
        f.write(f"| {r['order_uuid']} | {r['title']} | {r['created_at']} | {r['method']} | {r['path']} |\n")

print("Results saved to SUPP-1078.md")
