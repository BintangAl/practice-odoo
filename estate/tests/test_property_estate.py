from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.buyer = cls.env['res.partner'].create({
            'name' : 'Buyer',
        })

        cls.properties = cls.env['estate.property'].create([
           {
            'name': 'Big Villa', 
            'expected_price': 2000000,
           },
        ])

        cls.offers = cls.env['estate.property.offer'].create([
            {
                'price' : 2300000,
                'partner_id' : cls.buyer.id,
                'property_id' : cls.properties[0].id,
            }
        ])

    def test_action_sold(self):
        # Can't Sell a property with no accepted offers on it
        with self.assertRaises(UserError):
            self.properties.action_property_sold()

        # accept offer
        self.offers.action_offer_accepted()
        
        # Sell a property
        self.properties.action_property_sold()
        self.assertRecordValues(self.properties, [
            {'status' : 'sold'}
        ])

        # Can't create an offer for a sold property
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([
                {
                    'price' : 3000000,
                    'partner_id' : self.buyer.id,
                    'property_id' : self.properties[0].id
                }
            ])
