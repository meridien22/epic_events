from sources.models import User, Department
from sources.database import SessionLocal
from sources.setup_db import init_db
from sources.views import UserView
from sqlalchemy.exc import IntegrityError
import click

view = UserView()

@click.group()
def cli():
    click.clear()
    click.echo(click.style("=== EPIC EVENTS CRM ===", fg="cyan", bold=True))
    click.echo("-" * 23)

@cli.command()
@click.argument('name')
def add_department(name):
    """Ajouter un département."""
    with SessionLocal() as session:
        try:
            new_dept = Department(name=name)
            session.add(new_dept)
            session.commit()
            view.display_success(f"Département '{name}' créé.")
        except IntegrityError as e:
            session.rollback()
            view.display_error("Ce nom de département n'est pas autorisé ou déjà utilisé.")

        except Exception as e:
            session.rollback()
            view.display_error("Une erreur inattendue est survenue")

@cli.command()
@click.argument('first_name', type=click.STRING)
@click.argument('last_name', type=click.STRING)
@click.option('--email', default='oli@oli.fr', prompt=True, help="Email de l'utilisateur")
@click.option(
    '--password', 
    prompt=True, 
    hide_input=True, 
    confirmation_prompt=True,
    help="Mot de passe sécurisé"
)
def add_user(first_name, last_name, email, password):
    if len(first_name) > 50 or len(last_name) > 50:
        raise click.BadParameter("Le nom et le prénom ne doivent pas dépasser 50 caractères.")
    if "@" not in email or "." not in email:
        raise click.BadParameter("Le format de l'email est invalide.")
    
    with SessionLocal() as session:
        departments = session.query(Department).all()
        departments = {d.name: d.id for d in departments}
        
        choice = ", ".join([f"{v} ({k})" for k, v in departments.items()])
        department_id = click.prompt(
            "Veuillez choisir un département",
            type=click.Choice(choice)
        )

        try:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_id=department_id
            )
            new_user.set_password(password)
            
            session.add(new_user)
            session.commit()
            view.display_success(f"Utilisateur {first_name}  {last_name} créé.")
            
        except Exception as e:
            session.rollback()
            view.display_error("Impossible de créer cet utilisateur")

