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

    def _get_allowed_partner_ids(self):
        self.ensure_one()
        partner_ids = [self.partner_id.id]

        if self.has_group('copro_manager.group_supersyndic'):
            # Get partners through user relationships
            syndics = self.env['copro.syndic'].search([]).mapped('user_id.partner_id').ids
            copros = self.env['copro.coproprietaire'].search([]).mapped('user_id.partner_id').ids
            prestas = self.env['copro.prestataire'].search([]).mapped('user_id.partner_id').ids
            partner_ids += syndics + copros + prestas

        elif self.has_group('copro_manager.group_syndic'):
            # Get partners through user relationships
            supers = self.env['copro.supersyndic'].search([]).mapped('user_id.partner_id').ids
            copros = self.env['copro.coproprietaire'].search([]).mapped('user_id.partner_id').ids
            prestas = self.env['copro.prestataire'].search([]).mapped('user_id.partner_id').ids
            partner_ids += supers + copros + prestas

        elif self.has_group('copro_manager.group_coproprietaire'):
            # Use existing computed fields
            partner_ids += self.my_copro_supers.mapped('user_id.partner_id').ids
            partner_ids += self.my_copro_syndics.mapped('user_id.partner_id').ids
            prestas = self.env['copro.prestataire'].search([
                '|',
                ('supersyndic_id', 'in', self.my_copro_supers.ids),
                ('syndic_id', 'in', self.my_copro_syndics.ids)
            ]).mapped('user_id.partner_id').ids
            partner_ids += prestas

        elif self.has_group('copro_manager.group_prestataire'):
            # Use existing computed fields
            partner_ids += self.my_presta_supers.mapped('user_id.partner_id').ids
            partner_ids += self.my_presta_syndics.mapped('user_id.partner_id').ids
            copros = self.env['copro.coproprietaire'].search([
                '|',
                ('supersyndic_id', 'in', self.my_presta_supers.ids),
                ('syndic_id', 'in', self.my_presta_syndics.ids)
            ]).mapped('user_id.partner_id').ids
            partner_ids += copros

        return list(set(partner_ids))
        