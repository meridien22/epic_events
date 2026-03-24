import click
from tabulate import tabulate

class UserView:

    @staticmethod
    def display_success(message):
        click.echo(click.style(f"{message}", fg="green"))

    @staticmethod
    def display_error(message):
        click.echo(click.style(f"Erreur : {message}", fg="red"))

    @staticmethod
    def display_info(message):
        click.echo(click.style(f"{message}", fg="yellow"))

    @staticmethod
    def display_table(title, headers, data):
        click.echo(f"\n--- {title} ---")
        click.echo(tabulate(data, headers=headers, tablefmt="grid"))
  