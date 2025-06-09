# /home/siisi/property-management/dev/custom-addons/copro_manager/models/residence.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero
from odoo import _


class Residence(models.Model):
    _name = 'copro.residence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Informations sur la Résidence'
    _order = 'construction_date desc, name asc'

    name = fields.Char(string="Nom", required=True, tracking=True)
    address = fields.Text(string="Adresse", required=True)
    number_of_apartments = fields.Integer(string="Nombre d'appartements", required=True)
    total_area = fields.Float(string="Superficie Totale", required=True)
    construction_date = fields.Date(string="Date de Construction", tracking=True, required=True)
    number_of_floors = fields.Integer(string="Nombre d'étages", required=True)
    apartments_per_floor = fields.Float(
        string="Apartments/Floor",
        compute="_compute_apartments_per_floor",
        store=True
    )
    # Inverse One2many from apartment
    apartment_ids = fields.One2many(
        'copro.apartment', 'residence_id', string="Apartments"
    )
    common_areas = fields.Text(string="Zones Communes")
    heating_type = fields.Char(string="Type de Chauffage")
    last_inspection_date = fields.Date(string="Date du Dernier Contrôle")
    active = fields.Boolean(default=True, string="Active")

    # Relationships
    superuser_ids = fields.Many2many(
        'res.users',
        string='Super Users',
        relation='residence_superuser_rel',
        column1='residence_id',
        column2='user_id',
        tracking=True
    )
    supersyndic_ids = fields.Many2many(
        'copro.supersyndic', 
        string='Super Syndics',
        relation='residence_supersyndic_rel',
        column1='residence_id',
        column2='supersyndic_id',
        tracking=True,
        required=True
    )
    syndic_ids = fields.Many2many(
        'copro.syndic', 
        string='Syndics',
        relation='residence_syndic_rel',
        column1='residence_id',
        column2='syndic_id',
        tracking=True,
        required=True
    )
    coproprietaire_ids = fields.Many2many(
        'copro.coproprietaire', 
        string='Coproprietaires',
        relation='residence_coproprietaire_rel',
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

    def _compute_apartments_per_floor(self):
        for record in self:
            if record.number_of_floors > 0:
                record.apartments_per_floor = record.number_of_apartments / record.number_of_floors
            else:
                record.apartments_per_floor = 0

    @api.constrains('construction_date', 'last_inspection_date')
    def _check_dates(self):
        for record in self:
            if record.last_inspection_date and record.construction_date:
                if record.last_inspection_date < record.construction_date:
                    raise ValidationError("Inspection date cannot be before construction date!")

    @api.model
    def _check_tantieme_total(self, residence_ids):
        """
        Ensures the sum of tantièmes for each residence equals 1000.
        Called via XML `<function>`.
        """
        for res in self.browse(residence_ids):
            total = sum(res.apartment_ids.mapped('tantieme'))
            if not float_is_zero(total - 1000.0, precision_digits=2):
                raise ValidationError(
                    _("La somme des tantièmes dans %s doit être 1000, mais est %s.")
                    % (res.name, total)
                )

    def archive_residences(self):
        self.write({'active': False})
    
    def unarchive_residences(self):
        self.write({'active': True})

    def write(self, vals):
        # First perform the standard write
        res = super().write(vals)
        # If `active` was toggled on the residence, propagate it
        if 'active' in vals:
            # All records in `self` have the same write, so:
            for rec in self:
                # all apartments linked by the m2o
                m2o = rec.apartment_ids
                # all apartments linked by the m2m
                m2m = self.env['copro.apartment'].search([('residence_ids', 'in', rec.id)])
                (m2o | m2m).write({'active': vals['active']})

        return res

    # Keep your toggle helper if you need it
    def toggle_active(self):
        for rec in self:
            rec.write({'active': not rec.active})
