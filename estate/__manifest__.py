{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Admin",
    'category': 'Sales',
    'description': "",
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/property_offer_views.xml',
        'views/property_tag_views.xml',
        'views/property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_action.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}