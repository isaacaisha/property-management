# /home/siisi/super/odoo/scratch/addons/copro_manager/models/coproprietaire.py

from odoo import models, fields, api


class Coproprietaire(models.Model):
    _name = 'copro.coproprietaire'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Optional: For Odoo chatter
    _description = 'Copropriétaire'

    name = fields.Char(string="Nom", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Téléphone")
    address = fields.Text(string="Adresse")

    supersyndic_id = fields.Many2one('copro.supersyndic', string="Super Syndic Associé")
    syndic_id = fields.Many2one('copro.syndic', string="Syndic Associé", required=True)
    residence_id = fields.Many2one('copro.residence', string="Residence")
    apartment_id = fields.Many2one('copro.apartment', string="Apartment")
    user_id = fields.Many2one('res.users', string="Utilisateur", readonly=True, ondelete='cascade')

    @api.model
    def create(self, vals):
        if vals.get('email'):
            user_vals = {
                'name': vals.get('name'),
                'login': vals.get('email'),
                'email': vals.get('email'),
                'password': 'siisi321', # Default password

                # Assign both the base internal user group and your custom group
                'groups_id': [(6, 0, [
                    self.env.ref('base.group_user').id,
                    self.env.ref('copro_manager.group_coproprietaire').id
                ])],
            }
            user = self.env['res.users'].sudo().create(user_vals)
            vals['user_id'] = user.id  # Link user to coproprietaire

        # Create coproprietaire entry in the database
        coproprietaire = super(Coproprietaire, self).create(vals)
        return coproprietaire
