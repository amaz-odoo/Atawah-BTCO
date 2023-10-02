from odoo import fields,models

class floweshop(models.Model):
    _name = "floweshop"
    _description = "floweshop"


    flowerName = fields.Text()
    flowerSCName = fields.Text()
    season_start = fields.Date()
    season_end = fields.Date()
    frequenyWatering = fields.Integer()
    WateringAmount = fields.Integer()