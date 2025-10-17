import logging
from odoo import models, fields, api, _
from datetime import date, timedelta
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class GymAbonnement(models.Model):
    _name = "gym.abonnement"
    _rec_name = "member_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Abonnement du membre"

    type = fields.Selection([('mensuel', 'Mensuel'), ('annuel', 'Annuel')],
                            string="Type d’abonnement", required=True, tracking=True)
    prix = fields.Float(string="Prix", tracking=True)
    date_debut = fields.Date(string="Date de début", required=True, tracking=True)
    date_fin = fields.Date(string="Date de fin", required=True, tracking=True)
    member_id = fields.Many2one("gym.member", string="Membre", ondelete="cascade", tracking=True)
    state = fields.Selection([('active', 'Actif'), ('expired', 'Expiré')],
                             string="Statut", default='active', tracking=True)

    @api.constrains('date_debut', 'date_fin')
    def _check_date_inscription(self):
        for member in self:
            if member.date_debut and member.date_fin and member.date_fin < member.date_debut:
                raise ValidationError(_("La date de fin ne peut pas être avant la Date de début."))

    @api.model
    def _cron_expire_abonnements(self):
        _logger.info("===============debut de condition=============")
        today = date.today()
        _logger.info("===============today=============")
        _logger.info(today)
        abonnements = self.env['gym.abonnement'].sudo().search([('date_fin', '<', today), ('state', '=', 'active')])
        if abonnements:
            _logger.info("Abonne existe")

        for abo in abonnements.sudo():
            _logger.info("Debut de l'iteration")
            abo.state = 'expired'
            template = self.env.ref('gym.email_abonnement_expired', raise_if_not_found=False)
            if template:
                template.send_mail(abo.id, force_send=True, raise_exception=True, )
                _logger.info("Mail envoyer")
            else:
                _logger.info("Mail template non disponible")
            abo.message_post(body=f"Votre abonnement ({abo.type}) est maintenant expiré.", subject="Abonnement expiré")

    @api.model
    def check_expiring_abonnements(self):
        _logger.info("la fonction execute")
        today = date.today()
        _logger.info(today)
        target_date = today + timedelta(days=2)
        _logger.info(target_date)
        abonnements = self.search(
            [
                ('date_fin', '=', target_date),
                ('state', '=', 'active')
            ]
        )
        template = self.env.ref('gym_management.email_abonnement_expiring', raise_if_not_found=False)
        if template:
            for abo in abonnements.sudo():
                _logger.info("abonnement ", +abo.id)
                template.send_mail(abo.id, force_send=True)
                abo.message_post(
                    body=f"⚠️ Votre abonnement ({abo.type}) expire le {abo.date_fin}. Un email de rappel a été envoyé.",
                    subject="Rappel Abonnement")
        else:
            _logger.info("condition non retourne")


