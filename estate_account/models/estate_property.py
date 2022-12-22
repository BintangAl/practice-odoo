from odoo import Command, fields, models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_property_sold(self):
        self.env.user.check_access_rights('write')
        self.env.user.check_access_rule('write')

        # journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        journal = self.env['account.move'].sudo().with_context(default_move_type='out_invoice')._get_default_journal()

        for record in self:
            self.env['account.move'].sudo().create(
                {
                    "partner_id" : record.partner_id.id,
                    "move_type" : "out_invoice",
                    "journal_id" : journal.id,
                    "invoice_line_ids" : [
                        Command.create({
                            "name" : record.name,
                            "quantity" : 1,
                            "price_unit" : record.selling_price * 6 / 100
                        }),
                        Command.create({
                            "name" : "Administrative fees",
                            "quantity" : 1,
                            "price_unit" : 100
                        })
                    ]
                }
            )

        return super().action_property_sold()