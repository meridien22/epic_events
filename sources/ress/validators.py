from sources.ress.exceptions import FormError
import re

class Validators():

    @staticmethod
    def string_len(value, name, min, max):
        if len(value) < min or len(value) > max:
            raise FormError(f"Le nombre de caractère de {name} doit être compris entre {min} et {max}.")

    @staticmethod
    def email(value):
        if "@" not in value or "." not in value:
            raise FormError("Le format de l'email est invalide.")
        
    @staticmethod
    def valid_name(value):
        pattern = r"^[a-zA-ZÀ-ÿ\s]{3,}$"
        if not re.match(pattern, value):
            raise FormError("Ce nom n'est pas valide.")
        
    @staticmethod
    def valid_phone_number(value):
        pattern = r"^[\d()+ ]+$"
        if not re.match(pattern, value):
            raise FormError("Ce numéro de téléphone n'est pas valide.")
        
    @staticmethod
    def valid_password(value):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.?\":{}|<>-_]).{3,}$"
        if not re.match(pattern, value):
            raise FormError("Mot de passe non valide (au moins une minuscule, une majuscule et un caractère spécial).")
        
    @staticmethod
    def valid_amount(value):
        try:
            num = float(value)
            if num<0:
               raise FormError("Le montant n'est pas valide.") 
        except (ValueError, TypeError):
            raise FormError("Le montant n'est pas valide.")