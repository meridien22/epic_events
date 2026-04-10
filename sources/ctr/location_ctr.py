from sources.ctr.base_ctr import BaseCTR


class LocationCTR(BaseCTR):
    def __init__(self):
        """Defines the name of the DAO associated with the model."""
        super().__init__("location")
