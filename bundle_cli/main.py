import click
from bundle_cli.api import Bundle, NoResults, TooManyResults

# Global API client instance
api_client = Bundle()

@click.group()
def cli():
    """CLI tool for interacting with Bundle system using super-admin credential."""
    pass

@cli.command()
@click.option('--username', required=False, help='Your Bundle username.')
@click.option('--password', hide_input=True, required=False, help='Your Bundle password.')
def login(username, password):
    """Log in to the Bundle system."""
    try:
        api_client.login(username, password)
        role = api_client.user_info['role'] if api_client.user_info else 'Unknown'
        click.echo(f"Successfully logged in. Role: {role}")
    except Exception as e:
        click.echo(f"Login failed: {e}", err=True)

@cli.command()
@click.argument('query')
def search_client(query):
    """Search for a client by name."""
    try:
        api_client.login()
        api_client.select_client(search_for_client_name=query)
        click.echo(f"Client found UUID: {api_client.client_uuid}")
    except NoResults as e:
        click.echo(str(e))
    except TooManyResults as e:
        click.echo(str(e))
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)

@cli.command()
@click.argument('client_query')
@click.argument('order_query')
def search_order(client_query, order_query):
    """Search for an order. Requires client name and order reference."""
    try:
        api_client.login()
        api_client.select_client(search_for_client_name=client_query)
        order = api_client.select_order(order_reference=order_query)
        click.echo(f"Order found UUID: {api_client.order_uuid}")
        click.echo(f"Order details: {order}")
    except NoResults as e:
        click.echo(str(e))
    except TooManyResults as e:
        click.echo(str(e))
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)

if __name__ == '__main__':
    cli()
