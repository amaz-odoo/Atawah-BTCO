from odoo import fields,models

class MyModel(models.Model):
    _name = "my.model"
    _description = "My Model"


    flowerName = fields.Text()
    flowerSCName = fields.Text()
    season_start = fields.Date()
    season_end = fields.Date()
    frequenyWatering = fields.Integer()
    WateringAmount = fields.Integer()