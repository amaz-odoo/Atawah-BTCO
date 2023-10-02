from odoo import models, fields, api



class TrackingWater(models.Model):
    _name = 'flower.water'
    _description = 'Tracking watering times for flowers'
    _order = 'date'


    date = fields.Date(string='Date')
    serial_id = fields.Many2one("stock.lot", string="Serial No.")







