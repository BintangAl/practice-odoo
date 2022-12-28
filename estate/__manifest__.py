{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Admin",
    'category': 'Real Estate/Brokerage',
    'description': "",
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
        'views/res_users_views.xml',
        'views/property_offer_views.xml',
        'views/property_tag_views.xml',
        'views/property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_action.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
        'demo/demo_data.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license' : 'LGPL-3'
}