from bundle_cli import api

bundle = api.Bundle()
bundle.login()

print(bundle.user_info)