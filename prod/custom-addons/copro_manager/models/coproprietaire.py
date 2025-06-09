# /home/gestion/manage/crm/scratch/custom-addons/copro_manager/models/coproprietaire.py

from odoo import models, fields, api


class Coproprietaire(models.Model):
    _name = 'copro.coproprietaire'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Optional: For Odoo chatter
    _description = 'Copropriétaire'

    name = fields.Char(string="Nom", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Téléphone", required=True)
    # Related field: pull address from the residency record
    address = fields.Text(
        string="Adresse",
        related='residence_id.address',
        store=True,
        readonly=False,
    )

    supersyndic_id = fields.Many2one('copro.supersyndic', string="Super Syndic Associé", required=True)
    syndic_id = fields.Many2one('copro.syndic', string="Syndic Associé", required=True)
    residence_id = fields.Many2one('copro.residence', string="Residence", required=True)
    # Expose all apartments of the selected residence for display
    apartment_ids = fields.One2many(
        'copro.apartment',
        related='residence_id.apartment_ids',
        string="Apartments in Residence",
        readonly=True,
    )
    apartment_id = fields.Many2one('copro.apartment', string="Apartment", required=True)
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
