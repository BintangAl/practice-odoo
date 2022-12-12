from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

import datetime

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True,
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('strictly_positive_price', 'CHECK(price > 0)',
         'The offer price must be strictly positive'),
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.datetime.now() + datetime.timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_offer_accepted(self):
        for record in self:
            if record.property_id.status != 'canceled' and record.property_id.status != 'sold':
                record.property_id.offer_ids.status = 'refused'
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.partner_id = record.partner_id
                record.property_id.status = 'offer_accepted'
            else:
                raise UserError(record.property_id.status.capitalize() + ' properties cannot be accept offer')

        return True

    def action_offer_refused(self):
        for record in self:
            if record.property_id.status != 'canceled' and record.property_id.status != 'sold':
                if record.status == 'accepted':
                    record.property_id.selling_price = 0
                    record.property_id.partner_id = ''
                    record.property_id.status = 'offer_received'

                record.status = 'refused'
            else:
                raise UserError(record.property_id.status.capitalize() + ' properties cannot be refused offer')

        return True

    @api.ondelete(at_uninstall=False)
    def _check_status(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = 0
                record.property_id.partner_id = ''
