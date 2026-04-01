from sources.dao.base_dao import SessionLocal
from sources.dao import DAO
from sources.ctr.base_ctr import BaseCTR
from sources.ress.exceptions import DatabaseError


class LocationCTR(BaseCTR):
    def __init__(self):
        super().__init__("location")
