from odoo import models, fields, api
from collections import defaultdict



class FlowerShop(models.Model):
    _name = 'flower.type'
    _description = 'flowers shop types'

    common_name = fields.Char(string='Common Name', required='True')
    scientific_name = fields.Char(string='Scientific Name', required='True')
    watering_frequency = fields.Integer(string='Watering Frequency', help="Frequency is in number of days",
                                        required='True')
    watering_amount = fields.Float(string='Watering Amount (ml)', required='True')

    season_start = fields.Date(string='Season Start Date')
    season_end = fields.Date(string='Season End Date')
    sequence_id = fields.Many2one('ir.sequence', string='Flower Sequence')

    def name_get(self):
        return [(flower.id, "{} ({})".format(flower.scientific_name, flower.common_name)) for flower in self]


class Product(models.Model):
    _inherit = 'product.product'

    is_flower = fields.Boolean(string='Is Flower Product?')
    flower_id = fields.Many2one('flower.type', string='Flower')

    needs_watering = fields.Boolean(string="Needs Watering")
    flower_sequence_id = fields.Many2one('ir.sequence', related='flower_id.sequence_id')
    gardeners_ids = fields.Many2many('res.users', 'product_prod_users_rel', string='Assigned Gardeners')

    # Scheduled Action
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
