import requests
import logging

from odoo import models, fields, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    weather_ids = fields.One2many("stock.warehouse.weather", "warehouse_id", readonly=True)

    def _get_api_key_and_location(self, show_error):
        api_key = self.env["ir.config_parameter"].sudo().get_param("flower_shop.weather_api_key")
        if api_key == "unset" or not api_key:
            msg = _("Weather API key not found for Warehouse ID: {}".format(self.id))
            _logger.exception(msg)
            if show_error:
                raise UserError(msg)
        if not self.partner_id or not self.partner_id.partner_latitude or not self.partner_id.partner_longitude:
            msg = _("Location not found Warehouse ID: {}".format(self.id))
            _logger.exception(msg)
            if show_error:
                raise UserError(msg)
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
            msg = _("ERROR in Warehouse ID {}: {}".format(self.id, e))
            _logger.exception(msg)
            if show_error:
                raise UserError(msg)

    def get_weather_all_warehouses(self):
        for warehouse in self.search([]):
            warehouse.get_weather(show_error=False)

    def get_forecast_all_warehouses(self, show_error=True):
        flower_serials_to_water = self.env["stock.production.lot"]
        for warehouse in self:
            api_key, lat, lng = warehouse._get_api_key_and_location(show_error)
            url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(lat, lng, api_key)
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                entries = response.json()
                is_rainy_today = False
                # check only first 4 items in the list from 9 AM to 6 PM
                for i in range(0, 4):
                    if "rain" in entries["list"][i]:
                        rain = entries["list"][i]["rain"]["3h"]
                        if rain > 0.2:
                            is_rainy_today = True
                            break
                if is_rainy_today:
                    flower_products = self.env["product.product"].search([("is_flower", "=", True)])
                    quants = self.env["stock.quant"].search([
                        ("product_id", "in", flower_products.ids),
                        ("location_id", "=", warehouse.lot_stock_id.id)
                    ])
                    flower_serials_to_water |= quants.lot_id
            except Exception as e:
                msg = _("ERROR in Warehouse ID {}: {}".format(warehouse.id, e))
                _logger.exception(msg)
                if show_error:
                    raise UserError(msg)
        for flower_serial in flower_serials_to_water:
            self.env["flower.water"].create({
                "serial_id": flower_serial.id,
            })
