# -*- coding: utf-8 -*-

from datetime import datetime, time
import requests
from odoo.exceptions import ValidationError
from odoo import models, fields, api


class StockWarehouseWeather(models.Model):
    _name = 'stock.warehouse.weather'
    _description = 'Stock Warehouse Weather'
    _order = "capture_time"

    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse")

    temp = fields.Float(string="Temperature")
    pressure = fields.Float(string="Pressure")
    humidity = fields.Float(string="Humidity")
    wind_speed = fields.Float(string="Wind speed")
    rain_volume = fields.Float(string="Rain volume (for the past hour in mm)")
    description = fields.Char(string="Description")
    capture_time = fields.Datetime(string="Capture Time")


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    weather_ids = fields.One2many("stock.warehouse.weather", "warehouse_id")

    def _get_api_key_and_location(self, show_error):
        api_key = self.env["ir.config_parameter"].sudo(
        ).get_param("flower_shop.weather_api_key")
        if api_key == "unset" or not api_key:
            raise ValidationError(
                "API key is invalid. Please make sure you have set system parameters correctly.")
        if not self.partner_id or not self.partner_id.partner_latitude or not self.partner_id.partner_longitude:
            raise ValidationError(f"Warehouse location is not set properly for {self.name}.")
        return api_key, self.partner_id.partner_latitude, self.partner_id.partner_longitude

    def get_weather(self, show_error=True):
        self.ensure_one()
        api_key, lat, lng = self._get_api_key_and_location(show_error)
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(
            lat, lng, api_key)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            entries = response.json()
            self.env["stock.warehouse.weather"].create({
                "warehouse_id": self.id,
                "description": entries.get("weather")[0].get("description"),
                "pressure": entries.get("main").get("pressure"),
                "temp": entries.get("main").get("temp"),
                "humidity": entries.get("main").get("humidity") / 100,
                "wind_speed": entries.get("wind").get("speed"),
                "rain_volume": entries.get("rain").get("1h") if "rain" in entries else 0,
                "capture_time": fields.Datetime.now(),
            })
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Weather State has successfully updated!',
                    'type': 'rainbow_man',
                }
            }
        except Exception as e:
            raise ValidationError("Failed to load data from API")

    def get_weather_all_warehouses(self):
        for warehouse in self.search([]):
            warehouse.get_weather(show_error=False)

    def get_forecast_all_warehouses(self, show_error=True):
        self.ensure_one()
        api_key, lat, lng = self._get_api_key_and_location(show_error)
        url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(
            lat, lng, api_key)
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            entries = response.json()
            # Check weather data between 9 AM and 6 PM
            for entry in entries['list']:
                timestamp = entry['dt']
                dt = datetime.utcfromtimestamp(timestamp)
                rain = entry.get('rain', {}).get('3h', 0)  # Rain volume in mm
                # Check if it's between 9 AM and 6 PM and rain > 0.2 mm
                if time(9, 0) <= dt.time() <= time(18, 0) and rain > 0.2:
                    # Add flower.water records for all flowers in the warehouse
                    quants = self.env['stock.quant'].search([("product_id.is_flower", "=", True)])
                    for flower in quants:
                        self.env["flower.water"].create({
                            "serial_id": flower.lot_id.id,
                            "date": fields.Date.today(),
                            "rain_watering": True,
                        })
        except requests.exceptions.Timeout:
            raise ValidationError("Request timed out. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"Request error: {e}")
        except Exception as e:
            raise ValidationError("Failed to load forecast data from API")

    def get_forecast_weather_all_warehouses(self):
        for warehouse in self.search([]):
            warehouse.get_forecast_all_warehouses(show_error=False)
