from odoo import models, fields


class StockWarehouseWeather(models.Model):
    _name = "stock.warehouse.weather"
    _description = "Warehouse Weather"

    temperature = fields.Float()
    pressure = fields.Float()
    humidity = fields.Float()
    wind_speed = fields.Float()
    rain_volume = fields.Float()
    description = fields.Char()
    capture_time = fields.Datetime()
    warehouse_id = fields.Many2one("stock.warehouse")
