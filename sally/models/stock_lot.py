# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FlowerStockLot(models.Model):
    _inherit = "stock.lot"

    water_ids = fields.One2many("flower.water", "serial_id")
    is_flower = fields.Boolean(
        string='Is Flower Product?', related='product_id.is_flower')
    needs_watering = fields.Boolean(
        string='Needs Watering?', related='product_id.needs_watering')
    user_ids = fields.Many2many('res.users', string='Gardner')

    def action_water_flower(self):
        for record in self.filtered(lambda rec: rec.is_flower):
            today = fields.Date.today()
            if record.water_ids:
                last_watered_date = record.water_ids[0].date
                frequency = record.product_id.flower_id.watering_frequency
                if (today - last_watered_date).days < frequency:
                    raise ValidationError(
                        f"You shall not water this flower because it has been watered!\nYou may try again in {frequency-(today - last_watered_date).days} days.")
            self.env["flower.water"].create({
                "serial_id": record.id,
                "date": today,
                "gardner": self.env.user.id,
                "rain_watering": False,
            })
        self.env['sally.flowers'].action_needs_watering()

    def action_open_watering_times(self):
        view_form = self.env.ref('sally.watering_records_view_form')
        view_tree = self.env.ref('sally.watering_records_view_tree')

        return {
            'name': self.display_name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'flower.water',
            'views': [(view_tree.id, 'tree'), (view_form.id, 'form')],
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product = self.env["product.product"].browse(vals["product_id"])
            if product.sequence_id:
                vals["name"] = product.sequence_id.next_by_id()
        return super().create(vals_list)
