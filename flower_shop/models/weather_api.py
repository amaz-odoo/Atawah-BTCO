from odoo import models, fields, api
from odoo.exceptions import UserError

import requests

class StockWarehouseWeather(models.Model):
    _name = 'stock.warehouse.weather'
    _description = 'Stock Warehouse Weather'

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    description = fields.Char(string='Description')
    pressure = fields.Float(string='Pressure')
    temperature = fields.Float(string='Temperature')
    humidity = fields.Float(string='Humidity')
    wind_speed = fields.Float(string='Wind Speed')
    rain_volume = fields.Float(string='Rain Volume')
    capture_time = fields.Datetime(string='Capture Time')


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    partner_id = fields.Many2one('res.partner', 'Warehouse Location')
    def _get_api_key_and_location(self, show_error=False):
        api_key = self.env["ir.config_parameter"].sudo().get_param("flower_shop.weather_api_key")

        # Check if the API key is unset or missing.
        if api_key == "unset" or not api_key:
            if show_error:
                raise UserError("Weather API key is not set in configuration parameters.")
            else:
                return None, None, None

        if not self.partner_id or not self.partner_id.partner_latitude or not self.partner_id.partner_longitude:
            if show_error:
                raise UserError("Warehouse location data is missing.")
            else:
                return None, None, None

        # Return the retrieved API key and location data.
        return api_key, self.partner_id.partner_latitude, self.partner_id.partner_longitude

    def get_weather(self, show_error=True):
        self.ensure_one()
        api_key, lat, lng = self._get_api_key_and_location(show_error)
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lng, api_key)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            entries = response.json()

            self.env["stock.warehouse.weather"].create({
                "warehouse_id": self.id,
                "description": entries["weather"][0]["description"],
                "pressure": entries["main"]["pressure"],
                "temperature": entries["main"]["temp"],
                "humidity": entries["main"]["humidity"] / 100,
                "wind_speed": entries["wind"]["speed"],
                "rain_volume": entries["rain"]["1h"] if "rain" in entries else 0,
                "capture_time": fields.Datetime.now(),
            })
        except Exception as e:
            if show_error:
                raise UserError("An unexpected error occurred: {}".format(e))

    # Get Weather Data for All Warehouses (Hourly)
    def get_weather_all_warehouses(self):
        for warehouse in self.search([]):
            warehouse.get_weather(show_error=False)


    # Get Weather Forecast (Daily) for each warehouse location
    def get_forecast_all_warehouses(self, show_error=True):
            for warehouse in self.search([]):
                forecast_data = warehouse.get_weather(show_error=False)
                # Check the forecast data for rain volume between 9 AM and 6 PM.
                if self.is_rain_expected(forecast_data):
                    # Query flower stock in the warehouse.
                    flower_stock = warehouse.get_flower_stock()
                    # Water flowers if rain is expected.
                    warehouse.water_flowers(flower_stock)

    def is_rain_expected(self, forecast_data):
            # Check if rain volume exceeds 0.2 mm in any forecast entry.
            if forecast_data:
                for entry in forecast_data:
                    if entry.get('rain_volume', 0.0) > 0.2:
                        return True
            return False

    def get_flower_stock(self):
            flower_stock = self.env['stock.quant'].search([
                ('location_id', '=', self.lot_stock_id.id),
                ('product_id.is_flower', '=', True),
            ])
            return flower_stock

    def water_flowers(self, flower_stock):
            # Call a watering method on each flower in the stock.
            for quant in flower_stock:
                quant.product_id.water_flower()

    def open_weather_data(self):
        self.get_weather()
        return {
            'name': 'Weather Data',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.warehouse.weather',
            'view_mode': 'tree,form',
            'domain': [('warehouse_id', '=' , self.id)],
        }