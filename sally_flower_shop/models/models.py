from odoo import models, fields


class Flower(models.Model):
    _name = 'sally.flower'
    _description = 'Flower Information'

    common_name = fields.Char(string='Common Name', required=True)
    scientific_name = fields.Char(string='Scientific Name')
    season_start = fields.Date(string='Season Start Date')
    season_end = fields.Date(string='Season End Date')
    watering_frequency = fields.Integer(help="Frequency is in number of days")
    watering_amount = fields.Float(string='Watering Amount (ml)')
