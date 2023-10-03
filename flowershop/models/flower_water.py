from odoo import fields,models


class flowerwater(models.Model):
    
    _name = "flower_water"
    _description = "Flower Watering"
    _order = "date desc"

    serial_id = fields.Many2one("stock.lot")
    
    date= fields.Date(
        string="Last_date",  
        readonly=True 

    )
    
    
    
    
