from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    # _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_offer_view(self):
        return {
            'name': 'Porperty Offers',
            'view_mode': 'tree,form',
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',
            'domain': [('property_type_id', '=', self.id)],
            'context': {},
        }