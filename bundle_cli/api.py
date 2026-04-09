import requests
import json
import os
from dotenv import load_dotenv
from enum import Enum

from typing import Optional

class BadData(Exception):
  def __init__(self, data_in, accepted_values: list):
    self.message = f"{data_in} is bad. Accepted values are {accepted_values}."
    super().__init__(self.message)

class NoResults(Exception):
  def __init__(self, search_term: str):
    self.message = f"Searching for '{search_term}' gives 0 results."
    super().__init__(self.message)
  

class TooManyResults(Exception):
  def __init__(self, search_term: str, results: int):
    self.message = f"Searching for '{search_term}' gives {results} results. Try a less ambiguous search phrase."
    super().__init__(self.message)


class OrderStatus(Enum):
  PENDING = "pending"
  CREATED = "created"
  IN_PROGRESS = "in_progress"
  FINALISED = "finalised"
  CANCELLED = "cancelled"


class InventoryItemStatus(Enum):
  IN_STOCK = "in_stock"
  OUT_OF_STOCK = "out_of_stock"
  SOLD_OUT = "sold_out"


class WeightUnit(Enum):
  KG = "kg"
  G = "g"
  LB = "lb"
  OZ = "oz"
  # WEIRD STUFF THAT I HAVE TO ADD BELOW:
  KILOGRAM = "kilogram"


class DimensionUnit(Enum):
  MM = "mm"
  CM = "cm"
  M = "m"
  IN = "in"


def validate_kwargs(kwargs: dict, valid_config: dict):
  for key, value in kwargs.items():
    if key not in valid_config:
      raise KeyError(f"{key} is not allowed for this operation.")

    valid_data = valid_config[key]
    try:
      parsed_value = valid_data(value)
      if isinstance(parsed_value, Enum):
        kwargs[key] = parsed_value.value
      else:
        kwargs[key] = parsed_value
    except ValueError:
      valid_values = [e.value for e in valid_data]
      raise ValueError(f"Invalid value for {key}={kwargs[key]}. Valid data is {valid_values}")


class Bundle:
  def __init__(self):
    self.base_url = "https://api.bundle.wayfindr.io"
    self.session = requests.Session()
    self.session.headers.update({"Content-Type": "application/json", "Accept": "*/*"})
    self.access_token: Optional[str] = None
    self.session_info: Optional[str] = None
    self.user_info: Optional[str] = None
    self.client_list: Optional[list] = None
    self.client_uuid: Optional[str] = None
    self.client_info: Optional[dict] = None
    self.inventory_item_uuid: Optional[str] = None
    self.order_uuid: Optional[str] = None
    self.order_details: Optional[str] = None
    self.order_api_logs: Optional[list] = None
    self.shipment_uuid: Optional[str] = None
    self.default_query_params = {
      "page": 1,
      "per_page": 100,
    }
    
    self.cooldown = 1

  def login(self, username: Optional[str] = None, password: Optional[str] = None):
    '''
    Authenticate user and update session headers with the access token.
    '''
    if username == None or password == None:
      load_dotenv()
      username = os.getenv("BUNDLE_USERNAME")
      password = os.getenv("BUNDLE_PASSWORD")

    login_response = self.session.request(
        method="POST",
        url=f"{self.base_url}/auth-api/auth/admin/login",
        json={"email": username, "password": password},
    )
    login_response.raise_for_status()
    self.access_token = login_response.json()['data']["access_token"]
    self.session.headers.update({"Authorization": "Bearer " + self.access_token})
    self.session_info = login_response.json()
    self.user_info = {
        "uuid": self.session_info['data']['uuid'],
        "role": self.session_info['data']["role"],
    }

  def get_clients(self):
    '''
    Get all the clients (limit: 1000, maybe this should be updated in 2050)
    '''
    get_clients_response = self.session.request(
    method="GET",
    url=f"{self.base_url}/clients-api/admin/clients",
    params=self.default_query_params
      )
    get_clients_response.raise_for_status()
    if len(get_clients_response.json()['data']) > 0:
      self.client_list = get_clients_response.json()['data']
      return self.client_list
    else:
      return None

  
  def get_client_info(self, client_uuid: Optional[str] = None):
    client_uuid_data = self.client_uuid if client_uuid == None else client_uuid
    if client_uuid_data == None:
      return None

    get_client_info_request = self.session.request(
      method="GET",
      url=f"{self.base_url}/clients-api/admin/clients/{client_uuid_data}"
    )
    get_client_info_request.raise_for_status()
    self.client_info = get_client_info_request.json()["data"]
    return self.client_info



  def select_client(self, client_uuid: Optional[str] = None, search_for_client_name: Optional[str] = None):
    '''
    Select one client by uuid or client name.
    '''
    if search_for_client_name:
      search_for_client_response = self.session.request(
          method="GET",
          url=f"{self.base_url}/clients-api/admin/clients",
          params={"search": search_for_client_name},
      )
      search_for_client_response.raise_for_status()
      search_result = search_for_client_response.json()
      if search_result['meta']['totalItems'] == 0:
        raise NoResults(search_for_client_name)

      elif search_result['meta']['totalItems'] > 1:
        raise TooManyResults(search_for_client_name, search_result['meta']['totalItems'])

      else:
        self.client_uuid = search_result['data'][0]['uuid']

    elif client_uuid:
      self.client_uuid = client_uuid
    
    self.get_client_info()


  # search for inventory item and select if one found
  def select_inventory_item(self, inventory_item_uuid: Optional[str] = None, SKU_name: Optional[str] = None, supplier_tag: Optional[str] = None):
    '''
    Select one inventory item based on uuid or SKU name.
    '''
    if inventory_item_uuid:
      self.inventory_item_uuid = inventory_item_uuid
      # print("Inventory item", self.inventory_item_uuid, "selected.")
      return None

    elif SKU_name:
      search_for_sku_response = self.session.request(
          method="GET",
          url=f"{self.base_url}/orders-api/clients/{self.client_uuid}/products",
          params={"search": SKU_name, "supplier": supplier_tag},
      )
      search_for_sku_response.raise_for_status()
      search_result = search_for_sku_response.json()
      if search_result['meta']['totalItems'] == 0:
        raise NoResults(SKU_name)
        
      elif search_result['meta']['totalItems'] > 1:
        # try going through data to find an exact match
        for item in search_result['data']:
          if item['sku'] == SKU_name:
            self.inventory_item_uuid = item['uuid']
            return {
              "data": item
            }
        
        raise TooManyResults(SKU_name, search_result['meta']['totalItems'])
        
      else:
        self.inventory_item_uuid = search_result['data'][0]['uuid']
        return {
          "data": search_result['data'][0]
        }
      

  # update sku qty
  def update_sku_qty(self, qty: int):
    '''
    update the inventory qty of selected SKU
    '''
    if self.client_uuid and self.inventory_item_uuid:
      update_sku_qty_response = self.session.request(
          method="PATCH",
          url=f"{self.base_url}/orders-api/clients/{self.client_uuid}/products/{self.inventory_item_uuid}/quantity",
          json={"quantity": qty},
      )
      update_sku_qty_response.raise_for_status()
      update_result = update_sku_qty_response.json()
      return update_result


  def create_inventory_item(self, **kwargs):
    '''
    Create an inventory item
    '''
    # set a template
    valid_config = {
      "warehouse_uuid": str,
      "supplier": str,
      "sku": str,
      "title": str,
      "quantity": int,
      "quantity_allocated": int,
      "status": InventoryItemStatus,
      "weight_unit": WeightUnit,
      "weight": float,
      "price": float
    }

    validate_kwargs(kwargs, valid_config)
    for key, value in kwargs.items:
      if key not in valid_config:
        raise KeyError(f"{key} is not allowed for inventory data update.")

    valid_data = valid_config[key]
    try:
      parsed_value = valid_data(value)
      if isinstance(parsed_value, Enum):
        kwargs[key] = parsed_value.value
      else:
        kwargs[key] = parsed_value
    except ValueError:
      valid_values = [e.value for e in valid_data]
      raise ValueError(f"Invalid value for {key}={kwargs[key]}. Valid data is {valid_values}")

    if self.client_uuid == None:
      return None

    # TODO: "actual logic"


  def update_inventory_item_data(
    self, **kwargs):
    '''
    Update selected inventory item
    '''
    
    # set a template
    valid_config = {
      "warehouse_uuid": str,
      "supplier": str,
      "supplier_region": str,
      "sku": str,
      "title": str,
      "quantity": int,
      "quantity_allocated": int,
      "status": InventoryItemStatus,
      "weight_unit": WeightUnit,
      "weight": float,
      "price": float,
      "height": float,
      "width": float,
      "depth": float,
      "dimension_unit": DimensionUnit,
      "type": str,
      "hs_code": str
    }

    validate_kwargs(kwargs, valid_config)
    for key, value in kwargs.items():
      if key not in valid_config:
        raise KeyError(f"{key} is not allowed for inventory data update.")

      valid_data = valid_config[key]
      try:
        parsed_value = valid_data(value)
        if isinstance(parsed_value, Enum):
          kwargs[key] = parsed_value.value
        else:
          kwargs[key] = parsed_value
      except ValueError:
        valid_values = [e.value for e in valid_data]
        raise ValueError(f"Invalid value for {key}={kwargs[key]}. Valid data is {valid_values}")
      
    if self.inventory_item_uuid == None or self.client_uuid == None:
      return None

    edit_payload = kwargs
    inventory_item_edit_request = self.session.request(
      method="patch",
      url=f"{self.base_url}/orders-api/clients/{self.client_uuid}/products/{self.inventory_item_uuid}",
      json=edit_payload
    )
    inventory_item_edit_request.raise_for_status()
    return inventory_item_edit_request.json()

  def select_order(self, order_uuid: Optional[str] = None, order_reference: Optional[str] = None):
    '''
    Select an order by UUID or search for an order reference and select that order if only one result found.
    '''
    if order_uuid:
      self.order_uuid = order_uuid
    elif order_reference:
      select_order_request = self.session.request(
        method="GET",
        url=f"{self.base_url}/orders-api/clients/{self.client_uuid}/orders",
        params={
          "search": order_reference
        }
      )
      select_order_request.raise_for_status()
      search_result = select_order_request.json()
      if search_result['meta']['totalItems'] == 1:
        self.order_uuid = search_result["data"][0]['uuid']
      elif search_result['meta']['totalItems'] > 1:
        raise TooManyResults(order_reference, search_result['meta']['totalItems'])
      else:
        raise NoResults(order_reference)
    return search_result['data'][0]
  
  
  def get_order_details(self):
    '''
    Get all order details if order_uuid is selected.
    '''
    if self.order_uuid == None or self.client_uuid == None:
      return None
    else:
      get_order_request = self.session.request(
        method="GET",
        url=f"{self.base_url}/orders-api/clients/{self.client_uuid}/orders/{self.order_uuid}",
      )
      get_order_request.raise_for_status()
      self.order_details = get_order_request.json()
    return self.order_details


  def get_order_api_logs(self):
    '''
    Get all order's api logs
    '''
    if self.order_uuid == None or self.client_uuid == None:
      return None
    else:
      self.order_api_logs = []
      page = 1
      while True:
        get_order_api_logs_request = self.session.request(
          method="GET",
          url=f"{self.base_url}/orders-api/clients/{self.client_uuid}/orders/{self.order_uuid}/open-api-logs",
          params={
            "page": page,
            "per_page": 100,
            "column": "created_at",
            "desc": True
          }
        )
        get_order_api_logs_request.raise_for_status()
        self.order_api_logs.extend(get_order_api_logs_request.json()['data'])
        if get_order_api_logs_request.json()['meta']['totalPages'] > page:
          page +=1
        else:
          return self.order_api_logs


  def update_order_status(self, status):
    '''
    Update the order status to either Pending, Created, In Progress, Finalised, Cancelled
    '''
    accepted_values = ['pending', 'created', 'in_progress', 'finalised', 'cancelled']
    if status not in accepted_values:
      raise BadData(status, accepted_values)
    elif self.order_uuid == None or self.client_uuid == None:
      return None
    else:
      update_order_status_request = self.session.request(
        method="PATCH",
        url=f"{self.base_url}/orders-api/clients/{self.client_uuid}/orders/{self.order_uuid}/status",
        json={"status": status}
      )
      update_order_status_request.raise_for_status()
      return update_order_status_request.json()


  def get_shipment_list(self, status: Optional[str] = None):
    '''
    Get shipment list. Accepted status: 'created', 'in_transit', 'delivered', 'exception'
    '''
    accepted_values = ['created', 'in_transit', 'delivered', 'exception']
    
    if status is not None and status not in accepted_values:
      raise BadData(status, accepted_values)
    
    params = self.default_query_params.copy()
    if status is not None:
      params.update({"status": status})

    if self.client_uuid == None:
      return None
    else:
      data = []
      while True:
        shipment_list = self.session.request(
          method='GET',
          url=f"{self.base_url}/orders-api/clients/{self.client_uuid}/shipments",
          params=params,
        )
        shipment_list.raise_for_status()
        data.extend(shipment_list.json()['data'])
        metadata = shipment_list.json()['meta']
        if metadata['currentPage'] == metadata['totalPages']:
          return data
        else:
          params.update({"page": metadata['currentPage']+1})

  def reset_shipment(self):
    '''
    Reset selected shipment and put it back to "in_transit".
    '''

    if self.shipment_uuid == None:
      return None
    else:
      reset_shipment_request = self.session.request(
        method='POST',
        url=f'{self.base_url}/orders-api/clients/{self.client_uuid}/shipments/{self.shipment_uuid}/reset',
        json={
          "status": "in_transit"
        }
      )
      reset_shipment_request.raise_for_status()
      if reset_shipment_request.status_code == 200:
        return reset_shipment_request.json()


  def manage_user(self, user_uuid, add_client: Optional[str] = None, add_clients: Optional[list] = [], remove_client: Optional[str] = None, remove_clients: Optional[list] = []):
    '''
    Manage other users if your role is super-admin or admin. You can add or remove clients for other users, change their role to be either admin, manager, or user, change their timezone.
    '''
    if self.session_info['data']['role'] not in ['super-admin', 'admin']:
      raise PermissionError

    current_user_info = self.session.request(
      method="GET",
      url=f"{self.base_url}/users-api/admins/{user_uuid}"
    )
    current_user_info.raise_for_status()

    new_user_info_payload = {
      "first_name": current_user_info.json()['data']['first_name'],
      "last_name": current_user_info.json()['data']['last_name'],
      "timezone": current_user_info.json()['data']['timezone'],
      "role": current_user_info.json()['data']['role'],
      "client_uuid": [client['uuid'] for client in current_user_info.json()['data']['clients']]
    }
    
    if add_client:
      new_client_list = new_user_info_payload['client_uuid']
      new_client_list.append(add_client)
      new_user_info_payload['client_uuid'] = new_client_list

    if add_clients:
      new_client_list = new_user_info_payload['client_uuid']
      new_client_list.extend(add_clients)
      new_user_info_payload['client_uuid'] = new_client_list
    print(new_user_info_payload)
    
    if remove_client:
      new_client_list = new_user_info_payload['client_uuid']
      new_client_list.remove(remove_client)
      new_user_info_payload['client_uuid'] = new_client_list

    if remove_clients:
      new_client_list = new_user_info_payload['client_uuid']
      for client in remove_clients:
        new_client_list.remove(client)
      new_user_info_payload['client_uuid'] = new_client_list

    update_user_request = self.session.request(
      method="PATCH",
      url=f"{self.base_url}/users-api/admins/{user_uuid}",
      json=new_user_info_payload
    )
    update_user_request.raise_for_status()
    return update_user_request.json()
  

  def update_order_details(self, **kwargs):
    '''
    Update order details such as recipient name, recipient phone number, delivery address, etc.
    This function will also try to remove order lines without inventory_uuid because those lines will cause error when updating order. 
    Removed lines will be returned in case users want to add them back with correct data later.
    '''
    
    if self.order_uuid == None or self.client_uuid == None:
      return None
    
    valid_config = {
      "billing_address": dict,
      "shipping_address": dict,
      "note": str,
      "incoterms": str,
      "shipping_preference": str,
      "special_details": str,
      "packing_instructions": str,
      "order_lines": list
    }

    validate_kwargs(kwargs, valid_config)
    for key, value in kwargs.items():
      if key not in valid_config:
        raise KeyError(f"{key} is not allowed for order details update.")

      valid_data = valid_config[key]
      try:
        parsed_value = valid_data(value)
        kwargs[key] = parsed_value
      except ValueError:
        raise ValueError(f"Invalid value for {key}={kwargs[key]}. Valid data type is {valid_data}")
    
    self.get_order_details()
    if self.order_details == None:
      return None
    
    # try to remove order lines without inventory_uuid
    # because updating order with those lines will cause error.
    # removed lines will be returned in case users want to add them back with correct data later.
    new_item_lines_block = []
    removed_lines = []
    item_lines_block = self.order_details['data']['order_lines']
    for line in item_lines_block:
      if line['inventory_uuid'] != None:
        new_item_lines_block.append({"inventory_uuid": line['inventory_uuid'], "quantity": line['quantity'], "price": line['price']})
      else:
        removed_lines.append(line)


    update_order_details_payload = {
      "billing_address": kwargs.get("billing_address", self.order_details['data']['billing_address']),
      "shipping_address": kwargs.get("shipping_address", self.order_details['data']['shipping_address']),
      "note": kwargs.get("note", self.order_details['data']['note']),
      "incoterms": kwargs.get("incoterms", self.order_details['data']['incoterms']),
      "shipping_preference": kwargs.get("shipping_preference", self.order_details['data']['shipping_preference']),
      "special_details": kwargs.get("special_details", self.order_details['data']['special_details']),
      "packing_instructions": kwargs.get("packing_instructions", self.order_details['data']['packing_instructions']),
      "order_lines": new_item_lines_block
    }

    update_order_details_request = self.session.request(
      method="PATCH",
      url=f"{self.base_url}/orders-api/clients/{self.client_uuid}/orders/{self.order_uuid}",
      json=update_order_details_payload
    )
    update_order_details_request.raise_for_status()
    
    returned_data = {
      "new_data": update_order_details_request.json()
    }
    if len(removed_lines) > 0:
      returned_data["removed_lines"] = removed_lines
    
    return returned_data


class WooCommerce:
  def __init__(self):
    # TODO: "Make another object for WooCommerce"
    pass
