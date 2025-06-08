# /home/siisi/super/odoo/scratch/addons/copro_manager/models/prestataire.py

from odoo import models, fields, api


class Prestataire(models.Model):
    _name = "copro.prestataire"
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Optional: For Odoo chatter
    _description = "Prestataire"

    name = fields.Char(string="Nom", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Téléphone")
    address = fields.Text(string="Adresse")
    service_type = fields.Selection([
        ('plumber', 'Plomberie'),
        ('electrician', 'Électricité'),
        ('cleaning', 'Nettoyage'),
        ('security', 'Sécurité'),
        ('other', 'Autre'),
    ], string="Type de Service", required=True)

    supersyndic_id = fields.Many2one('copro.supersyndic', string="Super Syndic Responsable")
    syndic_id = fields.Many2one("copro.syndic", string="Syndic Responsable", required=True)
    residence_ids = fields.Many2many('copro.residence', string="Associated Residences")
    user_id = fields.Many2one('res.users', string="Utilisateur", readonly=True, ondelete='cascade')

    @api.model
    def create(self, vals):
        if vals.get('email'):
            user_vals = {
                'name': vals.get('name'),
                'login': vals.get('email'),
                'email': vals.get('email'),
                'password': 'siisi321',
                # Assign both the base internal user group and your custom group
                'groups_id': [(6, 0, [
                    self.env.ref('base.group_user').id,
                    self.env.ref('copro_manager.group_prestataire').id
                ])],
            }
            user = self.env['res.users'].sudo().create(user_vals)
            vals['user_id'] = user.id  # Link user to prestataire

        # Create prestataire entry in the database
        prestataire = super(Prestataire, self).create(vals)
        return prestataire
