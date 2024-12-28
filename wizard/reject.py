from odoo import models, fields


class RejectTerminationWizard(models.TransientModel):
    _name = 'reject.termination.wizard'
    _description = 'Comment'

    reason = fields.Text('Reason for Rejection', required=True)

    def action_confirm(self):
        ter_model = self.env['employee.termination']
        ter_record = ter_model.browse(self._context.get('active_id'))
        ter_record.cancel_resignation(self.reason)
        return {'type': 'ir.actions.act_window_close'}


