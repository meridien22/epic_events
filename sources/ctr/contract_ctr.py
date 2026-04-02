from sources.dao import DAO
from sources.ctr.base_ctr import BaseCTR
from sources.ress.exceptions import DatabaseError, FormError
from sources.dao.base_dao import SessionLocal
from sources.ress.validators import Validators
from sources.ress.exceptions import EpicEventsError
from sources.ress.token import current_session

class ContractCTR(BaseCTR):
    def __init__(self):
        super().__init__("contract")
 
    def get_table_with_headers(self, contracts):
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


    def add(self, client_id, total_amount):
        with SessionLocal() as session:
            try:
                dao = DAO(session)
                from sources.ctr import ctr
                ctr.client.exists(client_id)
                self.validate_attribute("total_amount", total_amount)
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

    def get_signature_status(self, contract):
        if contract.is_signed:
            return 'Oui'
        else:
            return 'Non'
        
    def set_attribute_contract(self, contract_id, attribute, value):
        try:
            self.validate_attribute(attribute, value)
            self.set_attribute(contract_id, attribute, value)
        except FormError as e:
            raise e
            
    def get_unassigned_contracts_for_current_commercial(self):
        user_id = current_session.user_id
        with SessionLocal() as session:
            dao = DAO(session)
            contracts = dao.contract.get_unassigned_contracts_for_commercial(user_id)
            return contracts

    def validate_attribute(self, attribute, value):
        match attribute:
            case "total_amount":
                Validators.valid_amount(value)
            case "remaining_amount":
                Validators.valid_amount(value)