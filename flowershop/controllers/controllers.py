# -*- coding: utf-8 -*-
# from odoo import http


# class Flowershop(http.Controller):
#     @http.route('/flowershop/flowershop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/flowershop/flowershop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('flowershop.listing', {
#             'root': '/flowershop/flowershop',
#             'objects': http.request.env['flowershop.flowershop'].search([]),
#         })

#     @http.route('/flowershop/flowershop/objects/<model("flowershop.flowershop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('flowershop.object', {
#             'object': obj
#         })
