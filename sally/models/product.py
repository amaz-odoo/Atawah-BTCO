# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FlowerProduct(models.Model):
    _inherit = 'product.product'
    
    flower_id = fields.Many2one('sally.flowers', string="Flower")
    is_flower = fields.Boolean(string='Is Flower Product?')
    needs_watering = fields.Boolean(string='Needs Watering?')
    sequence_id = fields.Many2one("ir.sequence", "Flower Sequence")
