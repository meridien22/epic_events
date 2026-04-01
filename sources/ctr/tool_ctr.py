# from sources.ress.exceptions import FormError
# import re

# class Tools():

#     @staticmethod
#     def get_choice_from_id_name(liste_):
#         liste_choice = {str(d.id): d.name for d in liste_}
#         menu_choice = "\n".join([f" [{k}] {v}" for k, v in liste_choice.items()])
#         return liste_choice, menu_choice
    
#     @staticmethod
#     def get_choice_from_field_update(dict_):
#         choices = []
#         for key in dict_:
#             choice = f"[{key}] {dict_[key][0]}"
#             choices.append(choice)
#         return "\n".join(choices)
    