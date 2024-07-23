# -*- coding: utf-8 -*-
# from odoo import http


# class Promotion(http.Controller):
#     @http.route('/promotion/promotion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/promotion/promotion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('promotion.listing', {
#             'root': '/promotion/promotion',
#             'objects': http.request.env['promotion.promotion'].search([]),
#         })

#     @http.route('/promotion/promotion/objects/<model("promotion.promotion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('promotion.object', {
#             'object': obj
#         })
