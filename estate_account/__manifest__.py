{
    'name': "Estate Account",
    'version': '1.0',
    'depends': ['base', 'estate', 'account'],
    'author': "Admin",
    'category': 'Sales',
    'description': "",
    # data files always loaded at installation
    'data': [
        'report/estate_property_templates.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license' : 'LGPL-3'
}