from odoo import fields,models 


class stockWarehouse(models.Model): 
    _name="stock.warehouse.weather"
    _order= 'capture_time desc '

    weather_rec = fields.Many2one('stock.warehouse',
        string='Weather record'
    )
    

    warehouse_id = fields.Integer(
        string='warehouse_id',
    )

    description = fields.Char(
        string='description"',
    )
    pressure = fields.Integer(
        string='pressure',
    )
    temperature = fields.Integer(
        string='temperature',
    )
    humidity = fields.Integer(
        string='humidity',
    )
    wind_speed = fields.Char(
        string='wind_speed',
    )
    rain_volume = fields.Integer(help="for the past hour in mm",
        string='rain_volume',
    )
    capture_time = fields.Datetime(
        string='capture_time'
    )


