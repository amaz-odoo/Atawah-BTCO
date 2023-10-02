# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api


class FlowerModel(models.Model):
    _name = 'sally.flowers'
    _description = 'Sally Flowers'
    _rec_name = 'name'

    name = fields.Char(string="Common Name")
    sci_name = fields.Char(string="Scientific Name")
    season_start= fields.Date(string="Season Start Date")
    season_end = fields.Date(string="Season End Date")
    watering_frequency = fields.Integer(string="Watering Frequency")
    watering_amount = fields.Float(string="Watering Amount")
    
    def name_get(self):
        return [(flower.id, "{} ({})".format(flower.sci_name, flower.name)) for flower in self]

    def action_needs_watering(self):
        flowers = self.env["product.product"].search([("is_flower", "=", True)])
        serials = self.env["stock.lot"].search([("product_id", "in", flowers.ids)])
        lot_vals = defaultdict(bool)
        for serial in serials:
            if serial.water_ids:
                last_watered_date = serial.water_ids[0].date
                frequency = serial.product_id.flower_id.watering_frequency
                today = fields.Date.today()
                needs_watering = (today - last_watered_date).days >= frequency
                lot_vals[serial.product_id.id] |= needs_watering
            else:
                lot_vals[serial.product_id.id] = True
        for flower in flowers:
            flower.needs_watering = lot_vals[flower.id]
    

class FlowerWater(models.Model):
    _name = "flower.water"
    _description = "Flower Watering"
    _rec_name = 'date'
    _order = "date"

    serial_id = fields.Many2one("stock.lot")
    date = fields.Date(string="Watering Date")
    gardner = fields.Many2one("res.users")
    rain_watering = fields.Boolean(string="Watered through rainy day", default=False)
