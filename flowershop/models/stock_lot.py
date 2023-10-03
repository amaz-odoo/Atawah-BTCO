from odoo import fields,models ,api
from odoo.exceptions import ValidationError



class stocklot(models.Model):
    _inherit = "stock.lot"

    water_ids = fields.One2many("flower_water", "serial_id")

    is_flower=fields.Boolean(related="product_id.is_flower")


    def action_water_flower(self):
        flowers = self.filtered(lambda rec: rec.is_flower)

        for record in flowers:
            if record.water_ids:
                last_watered_date = record.water_ids[0].date
                frequency = record.product_id.flower_ids.watering_frq
                today = fields.Date.today()
                if (today - last_watered_date).days < frequency:
                    raise ValidationError(f"Flower {record.name} Watered Recently!")
                    continue
            self.env["flower_water"].create({
            "serial_id": record.id,
            "date":fields.Date.today() })
    
    @api.model 
    def create(self, val):
        product = self.env["product.product"].browse(val["product_id"])
        if product.sequence_id:
            val["name"] = product.sequence_id.next_by_id()
        return super().create(val)   

    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product = self.env["product.product"].browse(vals["product_id"])
            if product.sequence_id:
                    vals["name"] = product.sequence_id.next_by_id()
        return super().create(vals_list)


    def action_open_watering_times(self):
        return{
        "type":"ir.actions.act_window",
        "name":"Watering Dates",
        "res_model":"flower_water",
        "view_mode":"tree",
        "domain":[('serial_id','=', self.name )]
        }
        
