from sources.dao import DAO
from sources.ctr.base_ctr import BaseCTR
from sources.ress.exceptions import FormError
from sources.ress.validators import Validators
from sources.ress.token import current_session
from sources.ress.context_manager import view_scope, transaction_scope


class ContractCTR(BaseCTR):
    def __init__(self):
        super().__init__("contract")

    def get_table_with_headers(self, contracts, commercial=False):
        table_data = []
        for contract in contracts:
            list = []
            list.append(contract.id)
            list.append(f"{contract.total_amount} €")
            list.append(f"{contract.remaining_amount} €")
            list.append(contract.date_creation)
            list.append("oui" if contract.is_signed else "non")
            list.append(f"{contract.client.first_name} {contract.client.last_name}")
            if commercial:
                list.append(f"{contract.client.commercial.email}")
            table_data.append(list)

        headers = [
            "ID",
            "Montant payé",
            "Montant à payer",
            "Date de création",
            "Signature",
            "Client",
        ]
        if commercial:
            headers . append("Commercial")
        return headers, table_data

    def add(self, client_id, remaining_amount):
        self.validate_attribute("remaining_amount", remaining_amount)
        with transaction_scope() as session:
            dao = DAO(session)
            from sources.ctr import ctr
            ctr.client.exists(client_id)
            dao.contract.create(
                client_id=client_id,
                remaining_amount=remaining_amount,
                total_amount=0,
            )

    def get_signature_status(self, contract):
        if contract.is_signed:
            return 'Oui'
        else:
            return 'Non'

    def set_attribute_contract(self, contract_id, attribute, value):
        self.validate_attribute(attribute, value)
        self.set_attribute(contract_id, attribute, value)

    def get_unassigned_contracts_for_current_commercial(self):
        user_id = current_session.user_id
        with view_scope() as session:
            dao = DAO(session)
            contracts = dao.contract.get_unassigned_contracts_for_commercial(user_id)
            return contracts

    def get_contracts_with_commercial(self):
        with view_scope() as session:
            dao = DAO(session)
            contracts = dao.contract.get_contracts_with_commercial()
            return contracts

    def validate_attribute(self, attribute, value):
        try:
            match attribute:
                case "total_amount":
                    Validators.valid_number_positive(value, "total_amount")
                case "remaining_amount":
                    Validators.valid_number_positive(value, "remaining_amount")
        except FormError as e:
            raise e
