from odoo import fields, models

class InheriteModel(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'user_id')

