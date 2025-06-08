# /home/siisi/super/odoo/scratch/addons/copro_manager/models/apartment.py

from odoo import models, fields, api


class Apartment(models.Model):
    _name = 'copro.apartment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Apartment'

    name = fields.Char(string="Apartment Name", required=True)
    number = fields.Char(string="Apartment Number", required=True)
    floor = fields.Integer(string="Floor")
    residence_id = fields.Many2one('copro.residence', string="Residence", ondelete='cascade')
    coproprietaire_ids = fields.One2many('copro.coproprietaire', 'apartment_id', string="Coproprietaires")

    # Relationships
    residence_ids = fields.Many2many(
        'copro.residence',
        relation='apartment_residence_rel',
        column1='supersyndic_id',
        column2='residence_id',
        string='Associated Residence'
    )
    superuser_ids = fields.Many2many(
        'res.users',
        string='Super Users',
        relation='apartment_superuser_rel',
        column1='residence_id',
        column2='user_id',
        tracking=True
    )
    supersyndic_ids = fields.Many2many(
        'copro.supersyndic', 
        string='Super Syndics',
        relation='apartment_supersyndic_rel',
        column1='residence_id',
        column2='supersyndic_id',
        tracking=True
    )
    syndic_ids = fields.Many2many(
        'copro.syndic', 
        string='Syndics',
        relation='apartment_syndic_rel',
        column1='residence_id',
        column2='syndic_id',
        tracking=True
    )
    coproprietaire_ids = fields.Many2many(
        'copro.coproprietaire', 
        string='Coproprietaires',
        relation='apartment_coproprietaire_rel',
        column1='residence_id',
        column2='coproprietaire_id',
        tracking=True
    )
    created_by = fields.Many2one(
        'res.users', 
        string='Created By', 
        default=lambda self: self.env.user,
        readonly=True,
        ondelete='set null'
    )
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now)
    extra_data = fields.Json(string='Extra Data')

    #@api.model
    #def create(self, vals):
    #    user = self.env.user  # Get the current user
    #    
    #    # Determine the role of the user and assign to created_by
    #    if user in self.env['copro.residence'].search([]).mapped('superuser_ids'):
    #        vals['created_by'] = user.id
    #    elif user in self.env['copro.residence'].search([]).mapped('supersyndic_ids'):
    #        vals['created_by'] = user.id
    #    elif user in self.env['copro.residence'].search([]).mapped('syndic_ids'):
    #        vals['created_by'] = user.id
    #    else:
    #        vals['created_by'] = user.id  # Default to current user if no specific role is found
#
    #    apartment = super(Apartment, self).create(vals)
    #    return apartment
