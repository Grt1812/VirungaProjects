from odoo import models, fields, api


class GymMember(models.Model):
    _name = "gym.member"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Membre du gymndryase"

    name = fields.Char(string="Nom complet", required=True, tracking=True)
    email = fields.Char(string="Email", tracking=True)
    date_inscription = fields.Date(string="Date d’inscription", default=fields.Date.today, tracking=True)
    active = fields.Boolean(string="Actif", default=True, tracking=True)

    abonnement_ids = fields.One2many("gym.abonnement", "member_id", string="Abonnements", tracking=True)

    @api.model
    def create(self, vals):
        res = super(GymMember, self).create(vals)
        res.send_welcome_mail()
        return res

    def send_welcome_mail(self):
        for member in self:
            member.message_post(
                body=f"Bienvenue {member.name} ! Votre inscription à la salle de sport a été enregistrée avec succès.",
                subject="Bienvenue au Gym"
            )
