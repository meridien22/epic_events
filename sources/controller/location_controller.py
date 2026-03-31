from sources.dao.base_dao import SessionLocal
from sources.dao import DAO
from sources.exceptions import DatabaseError

def get_dict_location():
    with SessionLocal() as session:
        dao = DAO(session)
        locations = dao.location.get_all()
        if not locations:
            raise DatabaseError("Aucune adresse trouvée.") 
        dict_ = {}
        for location in locations:
            dict_[location.id] = f"{location.street} {location.postal_code} {location.city} {location.country}"
        
        return dict_