# /home/gestion/manage/crm/scratch/custom-addons/copro_manager/models/charge_distribution.py

from odoo import models, fields, api


class CoproChargeDistribution(models.Model):
    _name = 'copro.charge.distribution'
    _description = 'Charge Distribution Line'

    charge_id = fields.Many2one('copro.charge', string="Charge")
    apartment_id = fields.Many2one('copro.apartment', string="Apartment")
    amount = fields.Float(string="Amount Due")
