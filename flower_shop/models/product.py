from collections import defaultdict

from odoo import fields, models


class Product(models.Model):
    _inherit = "product.product"

    is_flower = fields.Boolean("Is Flower Product?")
    flower_id = fields.Many2one("flower.flower")

    needs_watering = fields.Boolean(readonly=True)
    sequence_id = fields.Many2one("ir.sequence", "Flower Sequence")
    user_ids = fields.Many2many("res.users", string="Gardeners", domain=lambda self: [
        ("groups_id", "in", self.env.ref("flower_shop.group_gardener").ids)])

    def action_needs_watering(self):
        flowers = self.env["product.product"].search([("is_flower", "=", True)])
        serials = self.env["stock.production.lot"].search([("product_id", "in", flowers.ids)])
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
