# /home/siisi/property-management/dev/custom-addons/copro_manager/models/res_partner.py

from odoo import models, api
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def search(self, domain, offset=0, limit=None, order=None, count=False):
        user = self.env.user
        custom_groups = [
            'copro_manager.group_supersyndic',
            'copro_manager.group_syndic',
            'copro_manager.group_coproprietaire',
            'copro_manager.group_prestataire'
        ]
        
        if any(user.has_group(g) for g in custom_groups) and not self.env.is_admin():
            allowed_ids = user._get_allowed_partner_ids()
            domain = expression.AND([domain, [('id', 'in', allowed_ids)]])
        
        if count:
            return super().search_count(domain)
        return super().search(domain, offset=offset, limit=limit, order=order)
