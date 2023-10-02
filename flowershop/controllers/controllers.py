
from odoo import http


class Flowershop(http.Controller):
    @http.route('/flowershop', auth='public')
    def index(self, **kw):
        return "Hello, Ammar"
