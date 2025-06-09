# /home/gestion/manage/crm/scratch/custom-addons/copro_manager/models/res_users.py

from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    # all copro records (for coproprietaire users)
    copro_records = fields.One2many(
        'copro.coproprietaire', 'user_id',
        string="My Copro Records",
    )
    # all presta records (for prestataire users)
    presta_records = fields.One2many(
        'copro.prestataire', 'user_id',
        string="My Presta Records",
    )

    # → Supersyndics I may see as a copro user
    my_copro_supers = fields.Many2many(
        'copro.supersyndic', compute='_compute_my_copro_rel',
        string="My Copro’s Supersyndics",
    )
    # → Syndics I may see as a copro user
    my_copro_syndics = fields.Many2many(
        'copro.syndic', compute='_compute_my_copro_rel',
        string="My Copro’s Syndics",
    )

    # → Supersyndics I may see as a presta user
    my_presta_supers = fields.Many2many(
        'copro.supersyndic', compute='_compute_my_presta_rel',
        string="My Presta’s Supersyndics",
    )
    # → Syndics I may see as a presta user
    my_presta_syndics = fields.Many2many(
        'copro.syndic', compute='_compute_my_presta_rel',
        string="My Presta’s Syndics",
    )

    @api.depends('copro_records.supersyndic_id','copro_records.syndic_id',
                 'copro_records.supersyndic_id.syndic_ids')
    def _compute_my_copro_rel(self):
        for u in self:
            sup = u.copro_records.mapped('supersyndic_id')
            syn = u.copro_records.mapped('syndic_id') | sup.mapped('syndic_ids')
            u.my_copro_supers = sup
            u.my_copro_syndics = syn

    @api.depends('presta_records.supersyndic_id','presta_records.syndic_id',
                 'presta_records.supersyndic_id.syndic_ids')
    def _compute_my_presta_rel(self):
        for u in self:
            sup = u.presta_records.mapped('supersyndic_id')
            syn = u.presta_records.mapped('syndic_id') | sup.mapped('syndic_ids')
            u.my_presta_supers = sup
            u.my_presta_syndics = syn
