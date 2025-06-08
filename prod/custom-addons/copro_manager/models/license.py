# /home/siisi/super/odoo/scratch/addons/copro_manager/models/license.py

from odoo import models, fields, api
from odoo.exceptions import AccessError


class Licence(models.Model):
    _name = "copro.license"
    _description = "License"

    name = fields.Char(string="Nom de Licence", required=True)
    license_type = fields.Selection([
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('pro', 'Pro'),
    ], string="Type de Licence", required=True)
    license_start = fields.Date(string="Début le:", required=True)
    license_end = fields.Date(string="expire le:", required=True)

    @api.model
    def create(self, vals):
        if not self.env.user._is_superuser():
            raise AccessError("Only an Odoo superuser can assign a license.")

        # Create coproprietaire entry in the database
        license = super(Licence, self).create(vals)
        return license
        