from odoo import models, fields


class FlowerWater(models.Model):
    _name = "flower.water"
    _description = "Flower Watering"
    _order = "date"

    serial_id = fields.Many2one("stock.production.lot")
    flower_id = fields.Many2one("flower.flower", related="serial_id.product_id.flower_id")
    date = fields.Date(required=True, default=lambda self: fields.Date.today())
    common_name = fields.Char(related="flower_id.common_name")
    scientific_name = fields.Char(related="flower_id.scientific_name")
    serial = fields.Char(related="serial_id.name")
