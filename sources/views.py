import click

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