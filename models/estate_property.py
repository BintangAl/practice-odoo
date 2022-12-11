from odoo import api, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self: fields.Date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string = 'Garden Orientation', 
        selection = [
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
        ], 
        help="Orientation is used to indicate the position of the Park"
    )
    status = fields.Selection(
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default='new', 
        copy=False,
        required=True
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, string="Salesman")
    partner_id = fields.Many2one('res.partner',string='Buyer', readonly=True)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            try:
                record.best_price = max(offer.price for offer in record.offer_ids) #get maximum price of offer
            except:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_property_sold(self):
        for record in self:
            if record.status != 'canceled':
                record.status = 'sold'
            else:
                raise UserError('Canceled properties cannot be sold')

        return True

    def action_property_cancel(self):
        for record in self:
            if record.status != 'sold':
                record.status = 'canceled'
            else:
                raise UserError('Sold properties cannot be canceled')

        return True
    