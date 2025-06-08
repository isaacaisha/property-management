# /home/siisi/super/odoo/scratch/addons/copro_manager/models/syndic.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Syndic(models.Model):
    _name = 'copro.syndic'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Syndic'

    # Existing fields
    name = fields.Char(string="Nom du Syndic", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Téléphone")
    address = fields.Text(string="Adresse")
    
    supersyndic_id = fields.Many2one('copro.supersyndic', string="Super Syndic Associé")
    user_id = fields.Many2one('res.users', string="User Account", ondelete='set null')

    # Fields for license creation
    license_type = fields.Selection([
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('pro', 'Pro'),
    ], string="License Type")
    license_start = fields.Date(string="License Start Date")
    license_end = fields.Date(string="License End Date")
    license_id = fields.Many2one('copro.license', string="License")

    residence_ids = fields.Many2many(
        'copro.residence',
        relation='residence_syndic_rel',
        column1='syndic_id',
        column2='residence_id',
        string='Managed Residences'
    )
    apartment_id = fields.Many2one('copro.apartment', string="Apartment")
    
    @api.model
    def create(self, vals):
        # Create user for syndic if email is provided
        if vals.get('email'):

            user_vals = {
                'name': vals.get('name'),
                'login': vals.get('email'),
                'email': vals.get('email'),
                'password': 'siisi321',
                'groups_id': [(6, 0, [
                    self.env.ref('base.group_user').id,
                    self.env.ref('copro_manager.group_syndic').id
                ])],
            }
            user = self.env['res.users'].sudo().create(user_vals)
            vals['user_id'] = user.id  # Link user to syndic

        # Create syndic entry in the database
        syndic = super(Syndic, self).create(vals)
        return syndic
