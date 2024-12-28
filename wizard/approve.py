from odoo import models, fields, api


class ApproveTerminationWizard(models.TransientModel):
    _name = 'approve.termination.wizard'
    _description = 'Comment'

    reason = fields.Text('Reason for Approve', required=True)
    message_label = fields.Text()

    @api.model
    def default_get(self, fields):
        res = super(ApproveTerminationWizard, self).default_get(fields)
        if self.env.context.get('default_message_label'):
            res['message_label'] = self.env.context['default_message_label']
        return res

    def action_confirm(self):
        ter_model = self.env['employee.termination']
        ter_record = ter_model.browse(self._context.get('active_id'))
        if ter_record.state == 'submitted' or ter_record.state == 'hr':
            ter_record.manager_approved(self.reason)
        elif ter_record.state == 'init_manager':
            ter_record.initial_hr_approved(self.reason)
        elif ter_record.state == 'manager_approval':
            ter_record.it_approved(self.reason)
        elif ter_record.state == 'it_approval':
            ter_record.finance_approved(self.reason)
        elif ter_record.state == 'finance_approval':
            ter_record.legal_approved(self.reason)
        elif ter_record.state == 'legal_approval':
            ter_record.hr_employee_approved(self.reason)
        elif ter_record.state == 'hr_employee_approval':
            ter_record.hr_approved(self.reason)
        return {'type': 'ir.actions.act_window_close'}
