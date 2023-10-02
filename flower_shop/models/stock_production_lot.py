from odoo import models, fields, _, api
from odoo.exceptions import UserError


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    water_ids = fields.One2many("flower.water", "serial_id")
    is_flower = fields.Boolean(related="product_id.is_flower")

    def action_water_flower(self):
        flowers = self.filtered(lambda rec: rec.is_flower)
        bad_vals = []
        for record in flowers:
            if record.water_ids:
                last_watered_date = record.water_ids[0].date
                frequency = record.product_id.flower_id.watering_frequency
                today = fields.Date.today()
                if (today - last_watered_date).days < frequency:
                    bad_vals.append("[{}] {}".format(record.name, record.product_id.flower_id.common_name))
                    continue
            self.env["flower.water"].create({
                "serial_id": record.id,
            })
        self.env["product.product"].action_needs_watering()
        if bad_vals:
            self.env.cr.commit()
            raise UserError(_("Some flowers could not be watered. IDs={}".format(bad_vals)))

    def action_open_watering_times(self):
        self.ensure_one()
        return {
            "name": _("Watering Times"),
            "type": "ir.actions.act_window",
            "res_model": "flower.water",
            "view_mode": "list",
            "domain": [("id", "in", self.water_ids.ids)],
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product = self.env["product.product"].browse(vals["product_id"])
            if product.sequence_id:
                vals["name"] = product.sequence_id.next_by_id()
        return super().create(vals_list)
