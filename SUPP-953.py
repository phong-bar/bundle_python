from time import sleep
from bundle_cli import api

session = api.Bundle()
session.login()

users_to_modify = ["c8629958-8cb1-470b-af87-f59a5cd2aad1", "4bd1c97d-1313-4205-815e-c0645282f93b", "5fd213e9-9899-46f9-bab3-eae2c92cf44b"]
for user_id in users_to_modify:
    session.manage_user(user_id, add_client="4608bacf-93b1-49e7-85f0-445fb2e241c3")
    sleep(3)