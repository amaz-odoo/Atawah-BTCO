from odoo import models , fields,api

class FlowrProduct(models.Model):
    _inherit= "product.product"

    
    is_flower= fields.Boolean()
    flower_id=fields.Many2one("flower.shop")

    computed_watering= fields.Boolean()

    sequence_id = fields.Many2one("ir.sequence", "Flower Sequence")