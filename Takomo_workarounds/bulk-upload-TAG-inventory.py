import os
import sys
import pandas
import time
import random

folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(folder_path)

from bundle_cli import api, helper_functions


session = api.Bundle()
session.login()
session.select_client(search_for_client_name="Takomo")

excel_file_path = helper_functions.get_latest_file_in_folder(
    "Takomo_workarounds/TAG_inventory", file_extension="xlsx"
)

excel_file = pandas.read_excel(excel_file_path, skiprows=1, sheet_name="Sheet1")
excel_file.drop(["TYPE6", "TAG STYLE", "COLOR", "DIM", "SIZE"], axis=1, inplace=True)

not_found_SKUs_lines = []
for index, row in excel_file.iterrows():
    try:
        search_result = session.select_inventory_item(
            SKU_name=row["ITEM_NUMBER"], supplier_tag="TAG_US"
        )
    except Exception:
        not_found_SKUs_lines.append(index)
        print(f"{row['ITEM_NUMBER']} not found for TAG_US. Skipped.\033[K")
        continue
    print(f"{row['ITEM_NUMBER']:<20}", end=" | ")
    time.sleep(random.uniform(0.2, 1.0))
    print(f"{search_result['data']['uuid']}:", end=" ")
    before_value = int(search_result["data"]["quantity"])
    after_value = int(row["ALLOC ONHAND"])
    if after_value != before_value:
        print(f"before was {before_value}", end=" ")
        update_result = session.update_sku_qty(int(row["ALLOC ONHAND"]))
        print(f"now updated to {update_result['data']['quantity']}.", end=" ")
        print(f"[{after_value - before_value:+d}]")

        time.sleep(random.uniform(0.2, 1.0))
    else:
        print("Doesn't need updating. Skipped. \033[K\r", end="")
    time.sleep(random.uniform(0.2, 1.0))

if len(not_found_SKUs_lines) > 0:
    print(f"{len(not_found_SKUs_lines)} not found on Bundle.")
    for line in not_found_SKUs_lines:
        print(excel_file[line])
        continue
