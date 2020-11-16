from enum import Enum



class PersonaNaturalConstant(Enum):
    number_ruc = 0
    type_of_taxpayer = 1
    registration_name = 3
    registration_date = 4
    taxpayer_state = 5
    contributing_condition = 6
    tax_residence = 7
    economic_activity = 10


class PersonaJuridicaConstant(Enum):
    number_ruc = 0
    type_of_taxpayer = 1
    registration_name = 2
    registration_date = 3
    taxpayer_state = 4
    contributing_condition = 5
    tax_residence = 6
    economic_activity = 9