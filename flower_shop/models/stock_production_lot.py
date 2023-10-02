from odoo import fields, models, api
from odoo.exceptions import ValidationError


class StockProduction(models.Model):
    _inherit = 'stock.lot'

    is_flower = fields.Boolean(string='Is Flower Product?', related='product_id.is_flower')
    water_ids = fields.One2many("flower.water", "serial_id")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product = self.env["product.product"].browse(vals["product_id"])
            if product.flower_sequence_id:
                vals["name"] = product.flower_sequence_id.next_by_id()
        return super().create(vals_list)



    def action_water_flower(self):
        flowers = self.filtered(lambda rec: rec.is_flower)
        water_records = []
        for record in flowers:
            if record.water_ids:
                last_watered_date = record.water_ids[0].date
                frequency = record.product_id.flower_id.watering_frequency
                today = fields.Date.today()

                if (today - last_watered_date).days < frequency:
                    raise ValidationError(("Watering of flower %s is more frequent than allowed.") % record.id)
                continue

            water_records.append({
                "serial_id": record.id,
                "date": fields.Date.today(),
            })
        if water_records:
            self.env['flower.water'].create(water_records)

    # Smart Button--> Watering Times
    def action_open_watering_times(self):
        action = {
            'name': 'Watering Times',
            'type': 'ir.actions.act_window',
            'res_model': 'flower.water',
            'view_mode': 'tree,form',
            'domain': [('serial_id', '=', self.id)],
        }
        return action

