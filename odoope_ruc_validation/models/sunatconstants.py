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
    number_ruc = 5
    type_of_taxpayer = 6
    commercial_name = 8
    registration_date = 4
    taxpayer_state = 10
    contributing_condition = 11
    tax_residence = 12
    economic_activity = 13

class PersonaJuridicaConstant(Enum):
    number_ruc = 5
    type_of_taxpayer = 6
    commercial_name = 7
    registration_date = 3
    taxpayer_state = 9
    contributing_condition = 10
    tax_residence = 11
    economic_activity = 12