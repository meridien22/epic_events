import click
from tabulate import tabulate
import logging
import os
import sys


class View:
    """Manages displays in a terminal."""
    @staticmethod
    def display_success(message):
        """Displays a success message."""
        click.echo(click.style(f"{message}", fg="green"))

    @staticmethod
    def display_error(message):
        """Displays a error message."""
        click.echo(click.style(f"Erreur : {message}", fg="magenta"))

    @staticmethod
    def display_info(message):
        """Displays an information message."""
        click.echo(click.style(f"{message}", fg="yellow"))

    @staticmethod
    def display_table(title, headers, data):
        """Displays a table."""
        click.echo(click.style(f"{title}", fg="yellow"))
        View.display_separation_line()
        click.echo(tabulate(data, headers=headers, tablefmt="grid"))

    @staticmethod
    def display_epic_title():
        """Displays epic title."""
        title = "E P I C   E V E N T S   C R M"
        click.echo(click.style(title, fg="cyan", bold=True))

    @staticmethod
    def display_parameter(message):
        """Displays a parameter message."""
        click.echo(click.style(f"{message}", fg="green"))

    @staticmethod
    def display_line_return():
        """Displays a new line."""
        click.echo("\n")

    @staticmethod
    def display_separation_line():
        """Displays a separated line."""
        click.echo("-" * 63)

    @staticmethod
    def get_choice_dict(dict_):
        """Displays choice from a dictionary."""
        choices = []
        for key in dict_:
            choice = f"[{key}] {dict_[key]}"
            choices.append(choice)
        return "\n".join(choices)

    @staticmethod
    def display_prompt_choices(title, choices):
        """Displays prompt for choices."""
        return click.prompt(
            f"{title} :\n{View.get_choice_dict(choices)}\nVotre choix ",
            type=click.Choice(choices.keys()),
            show_choices=False
        )

    @staticmethod
    def display_prompt_date(title):
        """Displays prompt for a date."""
        return click.prompt(
            f"{title} (JJ/MM/AAAA)",
            type=click.DateTime(formats=["%d/%m/%Y"])
        )

    @staticmethod
    def display_prompt_int(title):
        """Displays prompt for a integer."""
        return click.prompt(
            title,
            type=click.INT
        )

    @staticmethod
    def display_prompt_note(title):
        """Displays prompt an note."""
        return click.prompt(
            title,
            type=click.STRING,
            default="",
            show_default=False
        )

    @staticmethod
    def display_prompt_string(title):
        """Displays prompt for a string."""
        return click.prompt(
            title,
            type=click.STRING
        )
    
    @staticmethod
    def log(message = None, pause = False, exit = False):
        format = '%(levelname)s: %(filename)s (ligne %(lineno)d): %(message)s'
        logging.basicConfig(format=format, level=logging.DEBUG, force=True)
        if message is None:
            logging.debug("", stacklevel=2)
        else :
            logging.debug(message, stacklevel=2)
        if pause :
            os.system("pause")
        if exit:
            sys.exit()
