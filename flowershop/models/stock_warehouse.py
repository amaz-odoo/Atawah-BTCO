from odoo import fields,models
from odoo.exceptions import UserError,ValidationError
import requests
from datetime import datetime,time



class Stockwarehouse(models.Model):
    
    _inherit = 'stock.warehouse'
 

    weather_ids = fields.One2many('stock.warehouse.weather',
    'weather_rec',
        string='weather')

    def _get_api_key_and_location(self, show_error):
        api_key = self.env["ir.config_parameter"].sudo().get_param("flower_shop.weather_api_key")

        if api_key == "unset" or not api_key:

            raise ValidationError("API KEY DOES NOT EXIST")

        if not self.partner_id or not self.partner_id.partner_latitude or not self.partner_id.partner_longitude:

            raise ValidationError(f"FAILED TO GET LAT AND LONG FOR WAREHOUSE :{self.name}" )

        return api_key, self.partner_id.partner_latitude, self.partner_id.partner_longitude

        
    def get_allcaptures(self):
                    return{
                "type":"ir.actions.act_window",
                "name":"All Captured Weather infos",
                "res_model":"stock.warehouse.weather",
                "view_mode":"tree",
                "domain":[('warehouse_id','=', self.id)]
                }

    def get_water(self):
        self.env["stock.lot"].action_water_flower()

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
            return{
                "type":"ir.actions.act_window",
                "name":"Currnet Weather",
                "res_model":"stock.warehouse.weather",
                "view_mode":"tree",
                "domain":[('capture_time','=', fields.Datetime.now())]
                }
        except Exception as e:
            raise UserError("Failed to get weather !")

    def get_weather_all_warehouses(self):
        for warehouse in self.search([]):
            warehouse.get_weather(show_error=False)


    def get_forecast(self, show_error=True):
        self.ensure_one()
        api_key, lat, lng = self._get_api_key_and_location(show_error)
        url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(lat, lng, api_key)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            entries = response.json()
            for record in entries['list']:
                rain=record.get('rain',{}).get('3h',0)
                timec=record['dt']
                dt=datetime.utcfromtimestamp(timec)
                if time(9,0) <=  dt.time() <= time(18,0) and rain > 0.2:

                    stock=self.env["stock.quant"].search([("product_id.is_flower", "=", True),("warehouse_id",'=',self.id)])
                    print(stock)
                    for flower in stock:
                        rec=self.env["stock.lot"].search([("product_id.name", "=", flower.product_id.name)])
                        for item in rec:
                            self.env["flower_water"].create({
                        "serial_id": item.id,
                        "date":fields.Date.today() })

        except Exception as e:
            raise UserError("Failed to get Forecast !")

    def get_forecast_all_warehouses(self, show_error=True):
        for warehouse in self.search([]):
            warehouse.get_forecast(show_error=False)
        