{
    'name': "Gym Management",
    'version': '1.0',
    'author': 'NDK Corporation',
    'website': 'https://ndk-corporation.tech',
    'category': 'Services/Gym',
    'summary': "Gestion des membres et abonnements d'une salle de sport",
    'depends': ['base','mail','base_automation'],
    'data': [
        "security/ir.model.access.csv",
        "views/gym_member_views.xml",
        "views/gym_abonnement_views.xml",
        "views/menu.xml",
        'data/mail_template.xml',
        'data/cron_jobs.xml',

        'data/ir_cron.xml',

    ],
}
