# /home/gestion/manage/crm/scratch/custom-addons/copro_manager/models/syndic.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Syndic(models.Model):
    _name = 'copro.syndic'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Syndic'

    # Existing fields
    name = fields.Char(string="Nom du Syndic", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Téléphone", required=True)
    address = fields.Text(string="Adresse")
    
    supersyndic_id = fields.Many2one('copro.supersyndic', string="Super Syndic Associé", required=True)
    user_id = fields.Many2one('res.users', string="User Account", ondelete='set null')

    # Show the SuperSyndic’s license on this record
    license_id     = fields.Many2one(
        'copro.license',
        related='supersyndic_id.license_id',
        readonly=True,
        store=True,
        string="License",
    )
    license_type   = fields.Selection(
        related='supersyndic_id.license_id.license_type',
        readonly=True,
        store=True,
        string="Type de Licence",
    )
    license_start  = fields.Date(
        related='supersyndic_id.license_id.license_start',
        readonly=True,
        store=True,
        string="Début de Licence",
    )
    license_end    = fields.Date(
        related='supersyndic_id.license_id.license_end',
        readonly=True,
        store=True,
        string="Fin de Licence",
    )
    
    coproprietaire_ids = fields.Many2many(
        'copro.coproprietaire',
        relation='syndic_coproprietaire_rel',
        column1='syndic_id',
        column2='coproprietaire_id',
        string='Managed Coproprietaires',
    )
    prestataire_ids = fields.Many2many(
        'copro.prestataire',
        relation='syndic_prestataire_rel',
        column1='syndic_id',
        column2='prestataire_id',
        string='Managed Prestataires',
    )

    residence_ids = fields.Many2many(
        'copro.residence',
        relation='syndic_residence_rel',
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
