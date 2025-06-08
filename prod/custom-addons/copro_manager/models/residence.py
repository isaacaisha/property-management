# /home/siisi/super/odoo/scratch/addons/copro_manager/models/residence.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Residence(models.Model):
    _name = 'copro.residence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Informations sur la Résidence'
    _order = 'construction_date desc, name asc'

    name = fields.Char(string="Nom", required=True, tracking=True)
    address = fields.Text(string="Adresse", required=True)
    number_of_apartments = fields.Integer(string="Nombre d'appartements")
    total_area = fields.Float(string="Superficie Totale")
    construction_date = fields.Date(string="Date de Construction", tracking=True)
    number_of_floors = fields.Integer(string="Nombre d'étages")
    apartments_per_floor = fields.Float(string="Apartments/Floor", compute="_compute_apartments_per_floor")
    common_areas = fields.Text(string="Zones Communes")
    active = fields.Boolean(default=True)
    heating_type = fields.Char(string="Type de Chauffage")
    last_inspection_date = fields.Date(string="Date du Dernier Contrôle")

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
        tracking=True
    )
    syndic_ids = fields.Many2many(
        'copro.syndic', 
        string='Syndics',
        relation='residence_syndic_rel',
        column1='residence_id',
        column2='syndic_id',
        tracking=True
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

    def archive_residences(self):
        self.write({'active': False})
    
    def unarchive_residences(self):
        self.write({'active': True})

    # Implement the toggle_active method
    def toggle_active(self):
        for record in self:
            record.active = not record.active
