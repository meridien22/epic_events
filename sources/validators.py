import click
from sources.command.views import UserView

view = UserView()

class Validators():

    @staticmethod
    def StringLen(value, name, min, max):
        if len(value) < min or len(value) > max:
            message = f"Le nombre de caractère de {name} doit être compris entre {min} et {max}."
            view.display_info(message)
            click.get_current_context().exit()

    @staticmethod
    def email(value):
        if "@" not in value or "." not in value:
            message="Le format de l'email est invalide."
            view.display_info(message)
            click.get_current_context().exit()