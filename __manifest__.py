{
    'name': 'EOS',
    'version': '1.0',
    'summary': 'Manage Employee Termination Process',
    'description': 'This module manages the termination process for employees.',
    'author': 'Ghaith Ahmed@Advicts',
    'website': 'https://advicts.com/',
    'category': 'Human Resources',
    'depends': ['base', 'mail', 'hr', 'hr_payroll', 'account', 'maintenance'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/resign_employee.xml',
        'wizard/reject.xml',
        'wizard/approve.xml',
        'views/employee_termination_views.xml',
        'views/Manager_approval.xml',
        'views/termination_sequence.xml',
        'reports/termination.xml',
    ],
    "web.assets_frontend": ["employee_termination/static/src/fonts/Bahij TheSansArabic-Plain.ttf"],
    "web.assets_qweb": ["employee_termination/static/src/fonts/Bahij TheSansArabic-Plain.ttf"],
    'application': True,
}
