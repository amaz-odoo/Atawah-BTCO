from odoo import fields,models,api
import collections

class Product(models.Model):
    _inherit = "product.product"

    is_flower=fields.Boolean(string="Is flower?",
    )
    flower_ids=fields.Many2one('flowershop',
    string="Flower",
    invisble= True
    )

    needs_watering = fields.Boolean(
    )
    
    user_ids = fields.Many2many('res.users',
        string='garderenrs',
      invisble= True
    )
    sequence_id = fields.Many2one("ir.sequence","flower sequence",
      invisble= True)
    

    def action_needs_watering(self):
        flowers = self.env["product.product"].search([("is_flower", "=", True)])
        serials = self.env["stock.lot"].search([("product_id", "in", flowers.ids)])
        lot_vals = collections.defaultdict(bool)
        for serial in serials:
            if serial.water_ids:
                last_watered_date = serial.water_ids[0].date
                frequency = serial.product_id.flower_ids.watering_frq
                today = fields.Date.today()
                needs_watering = (today - last_watered_date).days >= frequency
                lot_vals[serial.product_id.id] |= needs_watering
            else:
                lot_vals[serial.product_id.id] = True
        for flower in flowers:
            flower.needs_watering = lot_vals[flower.id]

    
        
    

    