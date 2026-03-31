import click
from tabulate import tabulate
from sources.controller.tool_controller import Tools

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

    @staticmethod
    def display_epic_title():
        title = "E P I C   E V E N T S   C R M"
        click.echo(click.style(title, fg="cyan", bold=True))

    @staticmethod
    def display_parameter(message):
        click.echo(click.style(f"{message}", fg="green"))

    @staticmethod
    def display_line_return():
        click.echo("\n")

    @staticmethod
    def display_separation_line():
        click.echo("-" * 63)

    @staticmethod
    def display_prompt_choices(title, choices):
        return click.prompt(
            f"{title} :\n{Tools.get_choice_dict(choices)}\nVotre choix ",
            type=click.Choice(choices.keys()),
            show_choices=False
        )
    
    @staticmethod
    def display_prompt_date(title):
        return click.prompt(
            f"{title} (JJ/MM/AAAA)",
            type=click.DateTime(formats=["%d/%m/%Y"])
        )

    @staticmethod
    def display_prompt_int(title):
        return click.prompt(
            title,
            type=click.INT
        )
    
    @staticmethod
    def display_prompt_note(title):
        return click.prompt(
            title,
            type=click.STRING,
            default="",
            show_default=False
        )