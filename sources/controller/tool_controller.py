from sources.exceptions import FormError

class Validators():

    @staticmethod
    def StringLen(value, name, min, max):
        if len(value) < min or len(value) > max:
            raise FormError(f"Le nombre de caractère de {name} doit être compris entre {min} et {max}.")

    @staticmethod
    def Email(value):
        if "@" not in value or "." not in value:
            raise FormError("Le format de l'email est invalide.")

class Tools():

    @staticmethod
    def get_choice_from_id_name(liste_):
        liste_choice = {str(d.id): d.name for d in liste_}
        menu_choice = "\n".join([f" [{k}] {v}" for k, v in liste_choice.items()])
        return liste_choice, menu_choice
