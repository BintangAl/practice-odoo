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
        'views/property_type_action.xml',
        'views/estate_property_views.xml',
        'views/estate_property_action.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}