# /home/gestion/manage/crm/scratch/custom-addons/copro_manager/models/charge.py

from odoo import models, fields, api


class CoproCharge(models.Model):
    _name = 'copro.charge'
    _description = 'Co-ownership Charge'

    name = fields.Char(string="Description", required=True)
    amount = fields.Float(string="Total Amount", required=True)
    date = fields.Date(string="Date", required=True)
    residence_id = fields.Many2one('copro.residence', string="Residence", required=True)
    distribution_line_ids = fields.One2many(
        'copro.charge.distribution', 'charge_id', string="Distribution Lines"
    )

    # — propagate the Residence’s managers down to the Charge
    supersyndic_ids = fields.Many2many(
        'copro.supersyndic',
        string="Supersyndics",
        related='residence_id.supersyndic_ids',
        readonly=True,
    )
    syndic_ids = fields.Many2many(
        'copro.syndic',
        string="Syndics",
        related='residence_id.syndic_ids',
        readonly=True,
    )

    def action_distribute_charges(self):
        for charge in self:
            # 1) remove any existing lines
            if charge.distribution_line_ids:
                charge.distribution_line_ids.unlink()
            # 2) compute new
            apartments = self.env['copro.apartment'].search([
                ('residence_ids', '=', charge.residence_id.id)
            ])
            total_tantieme = sum(apartment.tantieme for apartment in apartments)
            for apartment in apartments:
                amt = (charge.amount * apartment.tantieme) / total_tantieme if total_tantieme else 0.0
                self.env['copro.charge.distribution'].create({
                    'charge_id': charge.id,
                    'apartment_id': apartment.id,
                    'amount': amt,
                })

    def action_post_to_accounting(self):
        journal = self.env['account.journal'].search([('type', '=', 'purchase')], limit=1)
        for line in self.distribution_line_ids:
            self.env['account.move'].create({
                'move_type': 'entry',
                'date': self.date,
                'journal_id': journal.id,
                'line_ids': [
                    (0, 0, {  # Debit line (Expense)
                        'account_id': journal.default_account_id.id,
                        'debit': line.amount,
                        'credit': 0.0,
                    }),
                    (0, 0, {  # Credit line (Copropriétaire's liability)
                        'account_id': line.apartment_id.created_by.partner_id.property_account_payable_id.id,
                        'debit': 0.0,
                        'credit': line.amount,
                    }),
                ],
            })
