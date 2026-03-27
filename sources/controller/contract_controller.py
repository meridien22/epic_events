from sources.dao import DAO
from sources.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sources.controller.tool_controller import Validators
from sources.exceptions import EpicEventsError

def get_table_for_all_contracts():
    with SessionLocal() as session:
        dao = DAO(session)
        contracts = dao.contract.get_all()
        if not contracts:
            raise DatabaseError("Aucun contrat trouvé.") 
        table_data = []
        for contract in contracts:
            list = []
            list.append(contract.id)
            list.append(f"{contract.total_amount} €")
            list.append(f"{contract.remaining_amount} €")
            list.append(contract.date_creation)
            list.append("oui" if contract.is_signed else "non")
            list.append(f"{contract.client.first_name} {contract.client.last_name}")
            table_data.append(list)

        headers = [
            "ID",
            "Montant payé",
            "Montant à payer",
            "Date de création",
            "Signature",
            "Client",
        ]
        return headers, table_data

def add(client_id, total_amount):
    with SessionLocal() as session:
        try:
            dao = DAO(session)
            if not dao.client.exists(client_id):
                raise DatabaseError("Ce client n'existe pas.")
            # Validators.valid_amount(total_amount)
            # dao.contract.create(
            #     client_id=client_id,
            #     total_amount=total_amount,
            #     remaining_amount=0,
            # )
            # session.commit()
        except EpicEventsError as e:
            raise e
        except Exception as e:
           raise DatabaseError("Enregistrement impossible.")