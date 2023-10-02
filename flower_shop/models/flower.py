from odoo import models, fields


class Flower(models.Model):
    _name = "flower.flower"
    _description = "Flower"

    common_name = fields.Char()
    scientific_name = fields.Char()
    season_start_date = fields.Date()
    season_end_date = fields.Date()
    watering_frequency = fields.Integer(help="Frequency is in number of days")
    watering_amount = fields.Float("Watering Amount (ml)")

    def name_get(self):
        return [(flower.id, "{} ({})".format(flower.scientific_name, flower.common_name)) for flower in self]
