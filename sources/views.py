import click

class UserView:
    def display_success(self, message):
        click.echo(click.style(f"{message}", fg="green"))

    def display_error(self, message):
        click.echo(click.style(f"Erreur : {message}", fg="red"))