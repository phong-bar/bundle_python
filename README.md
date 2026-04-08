# Bundle Python CLI & API Client

A Python library and Command-Line Interface (CLI) built to interact with the Bundle API system (`api.bundle.wayfindr.io`). This project provides both a programmatic API wrapper and a convenient CLI tool for performing administration and operational tasks such as managing clients, analyzing inventory, verifying shipments, and tracking orders.

## Features

- **Programmatic API Wrapper (`bundle_cli/api.py`)**: 
  - Authenticate securely via login endpoints.
  - Manage and query `Clients` (retrieval, search).
  - Check and update `Inventory Items` (SKU quantity, statuses, weights, dimensions).
  - Interact with `Orders` and their API logs (select, retrieve details, update statuses).
  - Manage `Shipments` (list, filter by status, reset).
  - User and permission management (for super-admins).

- **Command-Line Interface (`bundle_cli/main.py`)**:
  - `login`: Log into the Bundle system and read back user roles.
  - `search-client`: Search for a client UUID using their name.
  - `search-order`: Discover order details using client names and order references.

## Requirements

The project uses the following dependencies:
- `requests`: HTTP library for interacting with the Bundle Rest API.
- `python-dotenv`: Loading environment variables securely.
- `click`: For rendering the rich command-line interface.

## Configuration

For convenience, you can configure your credentials via a local `.env` file rather than passing them on the command line every time:

```env
BUNDLE_USERNAME=your_email@example.com
BUNDLE_PASSWORD=your_secure_password
```

## Usage

### 1. Using the Command-Line Interface (CLI)

Run the CLI tool from your terminal.

```bash
# Log into the system
python -m bundle_cli.main login

# Or pass credentials directly (not recommended for secure environments)
python -m bundle_cli.main login --username your_email@example.com --password your_password

# Search for a client
python -m bundle_cli.main search-client "Client Name"

# Search for an order
python -m bundle_cli.main search-order "Client Name" "OrderReference123"
```

### 2. Using the API Programmatically

You can import the `Bundle` object into your own scripts for automation workflows:

```python
from bundle_cli.api import Bundle

bundle = Bundle()
bundle.login() # Uses credentials from .env
print(f"Logged in as: {bundle.user_info}")

# Get shipment list that are 'in_transit'
shipments = bundle.get_shipment_list(status='in_transit')
print(shipments)
```

## Structure

- `bundle_cli/api.py`: Contains the core `Bundle` class and enumerated exception handlers/types (e.g., `NoResults`, `OrderStatus`).
- `bundle_cli/main.py`: The `click` based CLI exposing operations to the end user.
- `requirements.txt`: Python package dependencies.
- `test.py`: Simple functional check for the current module functionality.
