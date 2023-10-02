from odoo import models, api


class FlowerSaleReport(models.AbstractModel):
    _name = 'report.flower_shop.report_sale_order'
    _description = 'Flower Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        sale_order = self.env['sale.order'].browse(docids)
        order_lines = sale_order.order_line.filtered(lambda line: line.product_id.is_flower)
        flowers = order_lines.mapped('product_id')

        return {
          'doc_model': 'sale.order',
          'docs': sale_order,
          'products': flowers,
        }
