from sources.dao import DAO
from sources.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sources.controller.tool_controller import Validators
from sources.exceptions import EpicEventsError
from sources.controller.token_controller import current_session

def get_table_for_all_contracts():
    with SessionLocal() as session:
        dao = DAO(session)
        contracts = dao.contract.get_all()
        if not contracts:
            raise DatabaseError("Aucun contrat trouvé.") 
        else:
            return get_table_headers(contracts)
        
def get_table_attribute_egal(attribute_name, value):
    with SessionLocal() as session:
        dao = DAO(session)
        contracts = dao.contract.filter_by_attribute_egal(attribute_name, value)
        if not contracts:
            raise DatabaseError("Aucun contrat trouvé.")
        else:
            return get_table_headers(contracts)

def get_table_attribute_not_egal(attribute_name, value):
    with SessionLocal() as session:
        dao = DAO(session)
        contracts = dao.contract.filter_by_attribute_not_egal(attribute_name, value)
        if not contracts:
            raise DatabaseError("Aucun contrat trouvé.")
        else:
            return get_table_headers(contracts)

def get_table_headers(contracts):
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
            Validators.valid_amount(total_amount)
            dao.contract.create(
                client_id=client_id,
                total_amount=total_amount,
                remaining_amount=0,
            )
            session.commit()
        except EpicEventsError as e:
            raise e
        except Exception as e:
           raise DatabaseError("Enregistrement impossible.")

def exists(id_contract):
    with SessionLocal() as session:
        dao = DAO(session)
        return dao.contract.exists(id_contract)
    
def get(id_contract):
    with SessionLocal() as session:
        dao = DAO(session)
        return dao.contract.get_by_id(id_contract)
    
def get_signature_status(contract):
    if contract.is_signed:
        return 'Oui'
    else:
        return 'Non'
    
def set_attribute(contract_id, attribute, new_value):
    with SessionLocal() as session:
        dao = DAO(session)
        contract = dao.contract.get_by_id(contract_id)
        setattr(contract, attribute, new_value)
        try :
            match attribute:
                case "total_amount" | "remaining_amount":
                    Validators.valid_amount(new_value)
                case _:
                    pass
            session.commit()
        except EpicEventsError as e:
            session.rollback()
            raise e
        except Exception as e:
            session.rollback()
            raise DatabaseError("Enregistrement impossible.")
        
def get_contracts_for_current_commercial():
    user_id = current_session.user_id
    with SessionLocal() as session:
        dao = DAO(session)
        contracts = dao.contract.get_contracts_for_commercial(user_id)
        return contracts

def get_dict_from_contracts(contracts):
        dict_ = {}
        for contract in contracts:
            dict_[contract.id] = f'{contract.date_creation} {contract.total_amount} {contract.client.first_name} {contract.client.last_name}'
        return dict_