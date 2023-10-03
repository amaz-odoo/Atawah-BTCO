# -*- coding: utf-8 -*-

from odoo import models, fields, api



class flowershop(models.Model):
    _name = 'flowershop'
    _description = 'Flower Shop'

    
    cname = fields.Char(
        string='Common Name',
        required=True
    )
    sname = fields.Char(
        string='Scientific Name',
          required=True
    )
    season_start = fields.Date(  required=True)
    season_end = fields.Date(  required=True)
    
    watering_frq = fields.Integer(
        string='Watering Frequency',help="Watered one Every (input) Days!",
          required=True
    )
    watering_amount = fields.Integer(
        string='Watering Amount',help="Milimeters",
          required=True
    )
    
    def name_get(self):
        return [(flower.id, "{} ({})".format(flower.sname, flower.cname)) for flower in self]

    
    
    