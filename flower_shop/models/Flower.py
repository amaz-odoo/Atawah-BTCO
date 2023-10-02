from odoo import models, fields,api


class FlowerShop(models.Model):
    _name= "flower.shop"
    _description= "Sally's Flower Shop"
    _rec_name="Common_Name"


    Common_Name = fields.Char()
    Scientific_Name = fields.Char()
    Watering_Frequency = fields.Integer()
    Watering_Amount= fields.Float()
    Season_Start_Date = fields.Date()
    Season_End_Date = fields.Date()

    def name_get(self):
        return [(flower.id, "{} ({})".format(flower.Scientific_Name,flower.Common_Name )) for flower in self]


class FlowerWAter(models.Model):
    _name="flower.water"
    _description="flower watering"
    _order="date"

    serial_id=fields.Many2one("stock.lot")
    date = fields.Date(String="watering date")

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


    # vals = [{
    # "name": "ABC123",
    # "product_id": 2,
    # "quantity": 1,
    # }, {
    # "name": "XYZ321",
    # "product_id": 3,
    # "quantity": 1,
    # }]
 
    
    # vals = {
    # "name": "JKL456",
    # "product_id": 5,
    # "quantity": 1,
    # }

   
    