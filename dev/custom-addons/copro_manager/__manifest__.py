# /home/siisi/property-management/dev/custom-addons/copro_manager/__manifest__.py

{
    'name': 'Property Manager',
    'version': '1.0',
    'category': 'Property Management',
    'summary': 'Gestion des copropriétés avec rôles et permissions',
    'author': 'Requin Tibùron',
    'website': 'https://property-manager.siisi.online',
    'depends': ['base', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/apps_menu.xml',
        #'views/contact_views.xml',
        'views/supersyndic_views.xml',
        'views/syndic_views.xml',
        'views/coproprietaire_views.xml',
        'views/prestataire_views.xml',
        'views/license_views.xml',
        'views/residence_views.xml',
        'views/apartment_views.xml',
        'views/charge_report_action.xml',
        'views/charge_views.xml',
        'views/charge_report_template.xml',
    ],
    'demo': [
        'demo/license_demo.xml',
        'demo/supersyndic_demo.xml',
        'demo/syndic_demo.xml',
        'demo/residence_demo.xml',
        'demo/apartment_demo.xml',
        'demo/charge_demo.xml',
        'demo/coproprietaire_demo.xml',
        'demo/prestataire_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # Add CSS/JS files here if you have them
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
