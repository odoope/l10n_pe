# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2019-TODAY OPeru.
#    Author      :  Grupo Odoo S.A.C. (<http://www.operu.pe>)
#
#    This program is copyright property of the author mentioned above.
#    You can`t redistribute it and/or modify it.
#
###############################################################################

from enum import Enum

class PersonaNaturalConstant(Enum):
    number_ruc = 0
    type_of_taxpayer = 1
    commercial_name = 3
    registration_date = 4
    taxpayer_state = 5
    contributing_condition = 6
    tax_residence = 7
    economic_activity = 10

class PersonaJuridicaConstant(Enum):
    number_ruc = 0
    type_of_taxpayer = 1
    commercial_name = 2
    registration_date = 3
    taxpayer_state = 4
    contributing_condition = 5
    tax_residence = 6
    economic_activity = 9