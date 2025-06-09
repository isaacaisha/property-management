# /home/gestion/manage/crm/scratch/custom-addons/copro_manager/models/supersyndic.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Supersyndic(models.Model):
    _name = 'copro.supersyndic'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Supersyndic'

    # Existing fields
    name = fields.Char(string="Nom du Super Syndic", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Téléphone", required=True)
    address = fields.Text(string="Adresse", required=True)
    user_id = fields.Many2one('res.users', string="User Account", ondelete='set null')
    syndic_ids = fields.One2many(
        'copro.syndic',
        'supersyndic_id',
        string='Managed Syndics',
    )
    coproprietaire_ids = fields.One2many(
        'copro.coproprietaire',
        'supersyndic_id',
        string='Managed Copropriétaires',
    )
    prestataire_ids = fields.One2many(
        'copro.prestataire',
        'supersyndic_id',
        string='Managed Prestataires',
    )
    
    residence_ids = fields.Many2many(
        'copro.residence',
        relation='residence_supersyndic_rel',
        column1='supersyndic_id',
        column2='residence_id',
        string='Managed Residences'
    )
    apartment_id = fields.Many2one('copro.apartment', string="Apartment")

    # Fields for license creation
    license_id = fields.Many2one('copro.license', string="License")

    license_type  = fields.Selection(
        related='license_id.license_type',
        readonly=True,
        string="Type de Licence",
    )
    license_start = fields.Date(
        related='license_id.license_start',
        readonly=True,
        string="Début de Licence",
    )
    license_end   = fields.Date(
        related='license_id.license_end',
        readonly=True,
        string="Fin de Licence",
    )

    @api.model
    def create(self, vals):
        # Extract license details from the vals dictionary
        license_type = vals.pop('license_type', None)
        license_start = vals.pop('license_start', None)
        license_end = vals.pop('license_end', None)
        existing_license_id = vals.get('license_id')

        # Validate license inputs: Check if both an existing license and new license details are provided
        new_license_details = any([license_type, license_start, license_end])
        if existing_license_id and new_license_details:
            raise ValidationError("Cannot set both an existing license and new license details.")
        if new_license_details and not all([license_type, license_start, license_end]):
            raise ValidationError("All license details (Type, Start, End) are required.")

        # Create user for supersyndic if email is provided
        if vals.get('email'):
            # Check if a user with this email already exists
            existing_user = self.env['res.users'].sudo().search([('login', '=', vals.get('email'))], limit=1)
            if existing_user:
                vals['user_id'] = existing_user.id
            user_vals = {
                'name': vals.get('name'),
                'login': vals.get('email'),
                'email': vals.get('email'),
                'password': 'siisi321',
                'groups_id': [(6, 0, [
                    self.env.ref('base.group_user').id,
                    self.env.ref('copro_manager.group_supersyndic').id
                ])],
            }
            user = self.env['res.users'].sudo().create(user_vals)
            vals['user_id'] = user.id

        # Create supersyndic entry in the database
        supersyndic = super(Supersyndic, self).create(vals)

        # Create a new license if new license details were provided
        if new_license_details:
            license_vals = {
                'name': f"License for {supersyndic.name}",
                'license_type': license_type,
                'start_at': license_start,
                'end_at': license_end,
            }
            # Create a new license and associate it with the supersyndic
            license = self.env['copro.license'].create(license_vals)
            supersyndic.license_id = license.id

        return supersyndic
