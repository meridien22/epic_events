# Epic Events

Epic Events est une entreprise de conseil et de gestion dans l'événementiel qui répond aux besoins des start-up voulant organiser des « fêtes épiques » .

Etapes à suivre pour installer localement l'application :

1. **Cloner le repository GitHub du projet**
    * `git clone https://github.com/meridien22/epic_events.git`
2. **Aller dans le répsertoire du projet**
    * `cd epic_events/`
3. **Si vous n'avez pas poetry sur votre machine, installez-le avec cette commande**
    * `curl -sSL https://install.python-poetry.org | python3 -`
4. **Créer l'environnement virtuel et installer les bilbiothèques**
    * `poetry config virtualenvs.in-project true`
    * `poetry install`