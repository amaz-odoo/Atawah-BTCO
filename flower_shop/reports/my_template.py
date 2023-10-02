from odoo import models,api

class MyTemplate(models.AbstractModel):
    _name="report.flower_shop.sale_order_id_flower"
    _description="My template"

    @api.model
    def _get_report_values(self, docids, data=None):
        report_name = 'flower_shop.sale_order_id_flower'
        report = self.env['ir.actions.report']._get_report_from_name(report_name)
        return {
            'doc_ids': docids,
            'doc_model': self.env[report.model],
            'docs': self.env[report.model].browse(docids),
            
        }
