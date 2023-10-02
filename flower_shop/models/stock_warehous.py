from odoo import fields,api,models
from odoo.exceptions import ValidationError

class StockWarhous(models.Model):
    _name="stock.warehous"
    _description="stock warhous"

    partner_id = fields.Many2one("res.partner")

    def _get_api_key_and_location(self, show_error):
        api_key = self.env["ir.config_parameter"].sudo().get_param("flower_shop.weather_api_key")
        if api_key == "unset" or not api_key:
            raise ValidationError(_('api_key does not exist or is not set!'))

        if not self.partner_id or not self.partner_id.partner_latitude or not self.partner_id.partner_longitude:
            raise ValidationError(_('latitude and longitude have some problems...'))

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
        except :
            ValidationError("In case it is empty or contains multiple records")

    def get_weather_all_warehouses(self):
        for warehouse in self.search([]):
            warehouse.get_weather(show_error=False)

        