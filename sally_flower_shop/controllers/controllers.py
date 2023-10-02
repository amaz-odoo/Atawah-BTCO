# -*- coding: utf-8 -*-
# from odoo import http


# class SallyFlowerShop(http.Controller):
#     @http.route('/sally_flower_shop/sally_flower_shop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sally_flower_shop/sally_flower_shop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sally_flower_shop.listing', {
#             'root': '/sally_flower_shop/sally_flower_shop',
#             'objects': http.request.env['sally_flower_shop.sally_flower_shop'].search([]),
#         })

#     @http.route('/sally_flower_shop/sally_flower_shop/objects/<model("sally_flower_shop.sally_flower_shop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sally_flower_shop.object', {
#             'object': obj
#         })
