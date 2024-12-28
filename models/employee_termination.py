import datetime
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

RESIGNATION_TYPE = [('resigned', 'Resignation'), ('fired', 'Termination')]


class EmployeeTermination(models.Model):
    _name = 'employee.termination'
    _description = 'End Of Services Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # ------------------------------------------- Fields ---------------------------------------------- #

    name = fields.Char(string='EOS Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))

    employee_id = fields.Many2one('hr.employee', string="Employee", default=lambda self: self.env.user.employee_id.id,
                                  help='Name of the employee for whom the request is creating',
                                  )

    department_id = fields.Many2one('hr.department', string="Department", related='employee_id.department_id',
                                    help='Department of the employee')

    manager_id = fields.Many2one(string="Manager", related='employee_id.parent_id',
                                 help='Department of the employee', store=True)

    coach_id = fields.Many2one(string="Coach", related='employee_id.parent_id',
                               help='Department of the employee')

    job_position = fields.Many2one(string="Job Position", related='employee_id.job_id', help='Position of the employee')

    image_128 = fields.Image(string="Image", related='employee_id.image_128')

    approved_submitted_date = fields.Date(string="Submitted Date",
                                          track_visibility="always")
    submitted_date = fields.Date(string="Submitted Date",
                                 track_visibility="always")
    submitted_by = fields.Many2one('hr.employee', string="Submitted By", store=True)

    approved_initial_manager_date = fields.Date(string="Initial Manager Approved Date",
                                                track_visibility="always")
    approved_initial_manager_by = fields.Many2one('hr.employee', string="initial manager approved By", store=True)

    approved_initial_hr_date = fields.Date(string="Initial HR Approved Date",
                                           track_visibility="always")
    approved_initial_hr_by = fields.Many2one('hr.employee', string="initial hr approved By", store=True)

    approved_revealing_date = fields.Date(string="Approved Last Day Of Employee",
                                          track_visibility="always")

    rejected_date = fields.Date(string="Rejected Date",
                                track_visibility="always")
    rejected_by = fields.Many2one('hr.employee', string="rejected By", store=True)

    resigned = fields.Boolean(default=False)
    approved_manager_date = fields.Date(string="Manager Approved Date",
                                        track_visibility="always")
    approved_manager_by = fields.Many2one('hr.employee', string="Manager Approved By", store=True)

    approved_it_date = fields.Date(string="IT Approved Date",
                                   track_visibility="always")
    approved_it_by = fields.Many2one('hr.employee', string="IT Approved By", store=True)

    approved_finance_date = fields.Date(string="Finance Approved Date",
                                        track_visibility="always")
    approved_finance_by = fields.Many2one('hr.employee', string="Finance Approved By", store=True)

    approved_law_date = fields.Date(string="Law Approved Date",
                                    track_visibility="always")
    approved_law_by = fields.Many2one('hr.employee', string="Law Approved By", store=True)

    approved_hr_employee_date = fields.Date(string="Hr Employee Approved Date",
                                            track_visibility="always")
    approved_hr_employee_by = fields.Many2one('hr.employee', string="Hr Employee Approved By", store=True)

    approved_hr_date = fields.Date(string="HR Approved Date",
                                   track_visibility="always")
    approved_hr_by = fields.Many2one('hr.employee', string="HR Approved By", store=True)
    start_date = fields.Date(string="Contract Start Date", store=True,
                             help='Start date of the Last contract')

    expected_revealing_date = fields.Date(string="Last Day of Employee", required=True,
                                          help='Employee requested date on which he is revealing from the company.')

    reason = fields.Text(string="Reason", required=True, help='Specify reason for leaving the company')

    resignation_type = fields.Selection(selection=RESIGNATION_TYPE, help="Select the type of resignation: normal "
                                                                         "resignation or fired by the company",
                                        default="resigned",
                                        )
    initial_manager_approved_reason = fields.Text(string="Initial Manager Approved Reason", track_visibility="always")
    initial_hr_approved_reason = fields.Text(string="Initial HR Approved Reason", track_visibility="always")
    manager_approved_reason = fields.Text(string="Manager Approved Reason", track_visibility="always")
    it_approved_reason = fields.Text(string="It Approved Reason", track_visibility="always")
    finance_approved_reason = fields.Text(string="Finance Approved Reason", track_visibility="always")
    legal_approved_reason = fields.Text(string="Legal Approved Reason", track_visibility="always")
    hr_approved_reason = fields.Text(string="HR Approved Reason", track_visibility="always")
    hr_employee_approved_reason = fields.Text(string="HR Employee Approved Reason", track_visibility="always")
    reject_reason = fields.Text(string="Reject Reason", track_visibility="always")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('init_manager', 'Initial Manager Approved'),
        ('hr', 'Initial HR Approved'),
        ('manager_approval', 'Manager Approved'),
        ('it_approval', 'IT Approved'),
        ('finance_approval', 'Finance Approved'),
        ('legal_approval', 'Legal Approved'),
        ('hr_employee_approval', 'Hr Employee approved'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')],
        default='draft', string='Status', track_visibility="always")

    read_only = fields.Boolean(string="check field")

    employee_contract = fields.Char(String="Contract", readonly=True, compute='check_request_existence', store=True)

    category_ids = fields.Many2many(
        'hr.employee.category', 'debugError',
        'emp', 'category_id',
        string='Tags')

    employee_id_readonly = fields.Boolean(compute='_compute_employee_id_readonly', store=True)
    end_date_readonly = fields.Boolean(compute='_compute_end_date_readonly', default=False)

    payslip_ids = fields.One2many('hr.payslip', 'employee_termination_id', string="Payslips",
                                  default=lambda self: self.onchange_employee_id())
    net_wage = fields.Float(string="Net Wage", compute='_compute_payslip_info')
    basic_wage = fields.Float(string="Basic Wage", compute='_compute_payslip_info')
    date_from = fields.Date(string="Date From", compute='_compute_payslip_info')
    reference = fields.Char(string="Reference", compute='_compute_payslip_info')
    payslip_run_id = fields.Many2one('hr.payslip.run', string="Payslip Run", compute='_compute_payslip_info')

    equipment_ids = fields.One2many('maintenance.equipment', 'employee_termination_id', string="Equipment",
                                    default=lambda self: self.onchange_employee_id())

    is_current_manager = fields.Boolean(compute='_compute_is_current_manager')

    @api.depends()
    def _compute_is_current_manager(self):
        for rec in self:
            if rec.manager_id.id == self.env.user.employee_id.id:
                rec.is_current_manager = True
            else:
                rec.is_current_manager = False

    # #################################### Methods ############################################### #
    def _compute_message_label(self):
        for rec in self:
            ms_label = ''
            if rec.state == 'submitted' or rec.state == 'hr':
                ms_label = "بيان موقف الموظف من ناحية التزامه بفترة الاشعار وتسليمه جميع المهام التي بذمته لمديره المباشر او الموظف البديل."
            elif rec.state == 'init_manager':
                ms_label = ""
            elif rec.state == 'manager_approval':
                ms_label = "بيان موقف الموظف من ناحية استلام الاجهزة الالكترونية التي بذمته او اي متعلق خاص بقسم نظم المعلومات تم تسليمه للموظف."
            elif rec.state == 'it_approval':
                ms_label = "بيان موقف الموظف من ناحية الذمة المالية في حال وجود اي سلف عمل او سلف شخصية بذمة الموظف مع التأكد من عدم تسليمه اي مواد او ذمم من المخازن والتأكد من جميع متعلقات القسم المالي مع الموظف."
            elif rec.state == 'finance_approval':
                ms_label = "بيان موقف الموظف في حال خروج الموظف بصورة رسمية مع التزامه بجميع السياسات ام خروجه من الشركة كان بطريقة مخالفة للسياسات والإجراءات المتبعة."
            elif rec.state == 'legal_approval':
                ms_label = "بيان موقف الموظف بعد التأكد من ان جميع الاقسام أتموا التأييد المطلوب منهم بصورة سليمة وصحيحة."
            elif rec.state == 'hr_employee_approval':
                ms_label = ""
            return ms_label

    def return_tree(self):
        return {
            'name': "EOS",
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'res_model': 'employee.termination',
            'target': 'main',
        }

    def action_notification(self, message):
        return {
            'type': "ir.actions.act_url",
            'target': 'new',
            'params': {
                'message': message,
                'type': 'success',
                'sticky': False
            }
        }

    def ter_submitted(self):
        if self.expected_revealing_date and self.start_date:
            if self.start_date >= self.expected_revealing_date:
                raise ValidationError(_('Last date of the Employee must be anterior to Joining date'))

            for rec in self:

                rec.submitted_date = str(datetime.now())
                rec.submitted_by = self.env.user.employee_id.id
                rec.read_only = True
                rec.state = 'submitted'
                if rec.resignation_type == 'resigned':
                    rec.resigned = True
                else:
                    rec.resigned = False

                rec.employee_id_readonly = True
                # Send a message with the custom message tag to the manager
                if rec.manager_id:
                    notification_subject = "EOS Request Submitted"
                    notification_body = "EOS request for %s has been submitted." % rec.employee_id.name

                    manager_partner = rec.manager_id.user_id.partner_id
                    if manager_partner:
                        rec.message_notify(
                            partner_ids=[manager_partner.id],  # Notify the manager's partner
                            subject=notification_subject,
                            body=notification_body,
                            record_name=rec.name,
                            model_name=self._description,
                        )

                        # Create an activity for the manager
                        activity_type_id = self.env['mail.activity.type'].search([('name', '=', 'EOS Request')])
                        rec.activity_schedule(
                            activity_type_id=activity_type_id.id,
                            summary="EOS Request",
                            note=f"EOS request for {rec.employee_id.name} has been submitted.",
                            user_id=rec.manager_id.user_id.id,
                        )
                    group = self.env['res.groups'].search([('name', '=', 'ter_notify_employee')], limit=1)
                    self.send_notification(rec, group, notification_subject, notification_body)
                    # self.action_notification('EOS Has Been Submitted')
                    return self.return_tree()

                else:
                    raise ValidationError(_('There is No Manager'))
        else:
            raise ValidationError(_('Please set joining date for employee'))
        return self.return_tree()

    def initial_manager_approved(self):
        self = self.sudo()
        termination_hr_group = self.env['res.groups'].search([('name', '=', 'ter_hr_employee')], limit=1)

        if termination_hr_group:
            # Get all users in the Termination group
            group_users = termination_hr_group.users

            for rec in self:
                rec.employee_id_readonly = True
                if self.env.user.employee_id == rec.manager_id or self.env.user.has_group(
                        "employee_termination.ter_admin_group"):
                    rec.state = 'init_manager'
                    rec.approved_initial_manager_date = str(datetime.now())
                    rec.approved_initial_manager_by = self.env.user.employee_id.id

                    for activity in self.activity_ids:
                        activity.sudo().action_feedback()

                    # Send a message and create an activity for each user in the group
                    notification_subject = "EOS Request Submitted"
                    notification_body = f"""EOS request for {rec.employee_id.name} has been submitted
                                            Initial HR approved by {rec.manager_id.name}."""

                    self.send_notification(rec, group_users, notification_subject, notification_body)
                    group = self.env['res.groups'].search([('name', '=', 'ter_notify_employee')], limit=1)
                    self.send_notification(rec, group, notification_subject, notification_body)

                else:
                    raise ValidationError("You Don't Have Access ,Because You are not the manager")

            return self.return_tree()

    def initial_hr_approved(self, reason):
        self = self.sudo()

        for rec in self:
            if self.env.user.has_group("employee_termination.ter_hr_employee_group") or self.env.user.has_group(
                    "employee_termination.ter_admin_group"):
                if rec.manager_id:
                    rec.state = 'hr'
                    rec.initial_hr_approved_reason = reason
                    rec.approved_initial_hr_date = str(datetime.now())
                    rec.approved_initial_hr_by = self.env.user.employee_id.id
                    for activity in self.activity_ids:
                        activity.sudo().action_feedback()
                    notification_subject = "EOS Request Submitted"
                    notification_body = f"EOS request for {rec.employee_id.name} has been submitted and" \
                                        f"Initial HR approved."

                    manager_partner = rec.manager_id.user_id.partner_id
                    if manager_partner:
                        rec.message_notify(
                            partner_ids=[manager_partner.id],  # Notify the manager's partner
                            subject=notification_subject,
                            body=notification_body,
                            record_name=rec.name,
                            model_name=self._description,
                        )

                        # Create an activity for the manager
                        activity_type_id = self.env['mail.activity.type'].search([('name', '=', 'EOS Request')])
                        rec.activity_schedule(
                            activity_type_id=activity_type_id.id,
                            summary="EOS Request",
                            note=f"EOS request for {rec.employee_id.name} has been submitted.",
                            user_id=rec.manager_id.user_id.id,
                        )
                    group = self.env['res.groups'].search([('name', '=', 'ter_notify_employee')], limit=1)
                    self.send_notification(rec, group, notification_subject, notification_body)
                else:
                    raise ValidationError(_('There is No Manager'))

            return self.return_tree()

    def manager_approved(self, reason):
        self = self.sudo()
        termination_it_group = self.env['res.groups'].search([('name', '=', 'ter_it')], limit=1)

        if termination_it_group:
            # Get all users in the Termination group
            group_users = termination_it_group.users

            for rec in self:
                rec.employee_id_readonly = True
                if self.env.user.employee_id == rec.manager_id or self.env.user.has_group(
                        "employee_termination.ter_admin_group"):
                    rec.state = 'manager_approval'
                    rec.manager_approved_reason = reason
                    rec.approved_manager_date = str(datetime.now())
                    rec.approved_manager_by = self.env.user.employee_id.id
                    for activity in self.activity_ids:
                        activity.sudo().action_feedback()

                    # Send a message and create an activity for each user in the group
                    notification_subject = "EOS Request Submitted"
                    notification_body = f"""EOS request for {rec.employee_id.name} has been submitted
                                            and Approve By The Manager {rec.manager_id.name}."""

                    self.send_notification(rec, group_users, notification_subject, notification_body)
                    group = self.env['res.groups'].search([('name', '=', 'ter_notify_employee')], limit=1)
                    self.send_notification(rec, group, notification_subject, notification_body)
                else:
                    raise ValidationError("You Don't Have Access ,Because You are not the manager")
                return self.return_tree()

    def it_approved(self, reason):
        self = self.sudo()
        termination_finance_group = self.env['res.groups'].search([('name', '=', 'ter_finance')], limit=1)

        if termination_finance_group:
            # Get all users in the Termination group
            group_users = termination_finance_group.users

            for rec in self:
                rec.employee_id_readonly = True
                if self.env.user.has_group("employee_termination.ter_it_group"):
                    equ_ids = self.env['maintenance.equipment'].search([('employee_id', '=', rec.employee_id.id)])
                    if equ_ids:
                        raise ValidationError(_('The Employee has Equipments belongings attached to him/her'))
                    rec.state = 'it_approval'
                    rec.it_approved_reason = reason
                    rec.approved_it_date = str(datetime.now())
                    rec.approved_it_by = self.env.user.employee_id.id
                    for activity in self.activity_ids:
                        activity.sudo().action_feedback()
                    # Send a message and create an activity for each user in the group
                    notification_subject = "EOS Request Submitted"
                    notification_body = f"""EOS request for {rec.employee_id.name} has been submitted
                                            and Approve By The Manager {rec.manager_id.name}.
                                            and Approved By IT"""

                    self.send_notification(rec, group_users, notification_subject, notification_body)
                    group = self.env['res.groups'].search([('name', '=', 'ter_notify_employee')], limit=1)
                    self.send_notification(rec, group, notification_subject, notification_body)
                else:
                    raise ValidationError("You Don't Have Access")
        return self.return_tree()

    def finance_approved(self, reason):
        self = self.sudo()

        termination_law_group = self.env['res.groups'].search([('name', '=', 'ter_law')], limit=1)

        if termination_law_group:
            # Get all users in the Termination group
            group_users = termination_law_group.users

            for rec in self:
                rec.employee_id_readonly = True
                if self.env.user.has_group("employee_termination.ter_finance_group"):

                    rec.state = 'finance_approval'
                    rec.finance_approved_reason = reason

                    rec.approved_finance_date = str(datetime.now())
                    rec.approved_finance_by = self.env.user.employee_id.id
                    for activity in self.activity_ids:
                        activity.sudo().action_feedback()
                    # Send a message and create an activity for each user in the group
                    notification_subject = "EOS Request Submitted"
                    notification_body = f"""EOS request for {rec.employee_id.name} has been submitted
                                                    and Approve By The Manager {rec.manager_id.name}.
                                                    , Approved By IT
                                                    and Approved By Finance"""

                    self.send_notification(rec, group_users, notification_subject, notification_body)
                    group = self.env['res.groups'].search([('name', '=', 'ter_notify_employee')], limit=1)
                    self.send_notification(rec, group, notification_subject, notification_body)
                else:
                    raise ValidationError("You Don't Have Access")

            return self.return_tree()

    def legal_approved(self, reason):
        self = self.sudo()

        term_hr_group = self.env['res.groups'].search([('name', '=', 'ter_hr_employee')], limit=1)

        if term_hr_group:
            # Get all users in the Termination group
            group_users = term_hr_group.users

            for rec in self:
                rec.employee_id_readonly = True
                if self.env.user.has_group("employee_termination.ter_law_group"):
                    rec.state = 'legal_approval'
                    rec.legal_approved_reason = reason
                    rec.approved_law_date = str(datetime.now())
                    rec.approved_law_by = self.env.user.employee_id.id
                    for activity in self.activity_ids:
                        activity.sudo().action_feedback()

                    # Send a message and create an activity for each user in the group
                    notification_subject = "EOS Request Submitted"
                    notification_body = f"""EOS request for {rec.employee_id.name} has been submitted
                                                    and Approve By The Manager {rec.manager_id.name}.
                                                    , Approved By IT Department
                                                    , Approved By Finance Department
                                                    and Approved By Legal Department"""

                    self.send_notification(rec, group_users, notification_subject, notification_body)
                    group = self.env['res.groups'].search([('name', '=', 'ter_notify_employee')], limit=1)
                    self.send_notification(rec, group, notification_subject, notification_body)
                else:
                    raise ValidationError("You Don't Have Access")
            return self.return_tree()

    def hr_employee_approved(self, reason):
        self = self.sudo()

        term_hr_group = self.env['res.groups'].search([('name', '=', 'ter_hr')], limit=1)

        if term_hr_group:
            # Get all users in the Termination group
            group_users = term_hr_group.users

            for rec in self:
                rec.employee_id_readonly = True
                if self.env.user.has_group("employee_termination.ter_hr_employee_group"):
                    rec.state = 'hr_employee_approval'
                    rec.hr_employee_approved_reason = reason
                    rec.approved_hr_employee_date = str(datetime.now())
                    rec.approved_hr_employee_by = self.env.user.employee_id.id
                    for activity in self.activity_ids:
                        activity.sudo().action_feedback()

                    # Send a message and create an activity for each user in the group
                    notification_subject = "EOS Request Submitted"
                    notification_body = f"""EOS request for {rec.employee_id.name} has been submitted
                                                    and Approve By The Manager {rec.manager_id.name}.
                                                    , Approved By IT Department
                                                    , Approved By Finance Department
                                                    , Approved By Legal Department
                                                    and Approved By hr employee"""

                    self.send_notification(rec, group_users, notification_subject, notification_body)
                    group = self.env['res.groups'].search([('name', '=', 'ter_notify_employee')], limit=1)
                    self.send_notification(rec, group, notification_subject, notification_body)
                else:
                    raise ValidationError("You Don't Have Access")
            return self.return_tree()

    def cancel_resignation(self, reason):
        self = self.sudo()

        termination_hr_group = self.env['res.groups'].search([('name', '=', 'ter_hr')], limit=1)

        if termination_hr_group:
            # Get all users in the Termination group
            group_users = termination_hr_group.users

            for rec in self:
                rec.state = 'rejected'
                rec.reject_reason = reason
                rec.rejected_date = str(datetime.now())
                rec.rejected_by = self.env.user.employee_id.id
                for activity in self.activity_ids:
                    activity.sudo().action_feedback()
                # Send a message and create an activity for each user in the group
                notification_subject = "EOS Request Rejected"
                notification_body = f"""EOS request for {rec.employee_id.name} has been rejected
                                                by {self.env.user.employee_id.id}"""

                self.send_notification(rec, group_users, notification_subject, notification_body)
            return self.return_tree()

    def hr_approved(self, reason):
        self = self.sudo()

        for rec in self:
            if self.env.user.has_group("employee_termination.ter_hr_group"):
                if rec.expected_revealing_date:
                    no_of_contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
                    rec.approved_revealing_date = str(datetime.now())
                    rec.approved_hr_date = str(datetime.now())
                    for contracts in no_of_contract:
                        if contracts.state == 'open':
                            rec.employee_contract = contracts.name
                            contracts.state = 'close'
                            rec.state = 'approved'

                    rec.state = 'approved'
                    rec.hr_approved_reason = reason
                    rec.approved_hr_date = str(datetime.now())
                    rec.approved_hr_by = self.env.user.employee_id.id
                    for activity in self.activity_ids:
                        activity.sudo().action_feedback()
                    # Changing state of the employee if resigning today

                    if rec.employee_id.active:
                        rec.employee_id.active = False
                        # employee=self.env['hr.employee'].search([('id', '=', rec.employee_id)], limit=1)
                        rec.employee_id.departure_date = rec.approved_hr_date
                        # Changing fields in the employee table with respect to resignation
                        if rec.resignation_type == 'resigned':
                            rec.employee_id.departure_reason_id = 2
                        else:
                            rec.employee_id.departure_reason_id = 1
                        # Removing and deactivating user
                        if rec.employee_id.user_id:
                            rec.employee_id.user_id.active = False
                            rec.employee_id.user_id = None
                    notification_subject = "EOS Request Approved"
                    notification_body = f"""EOS request for {rec.employee_id.name} has been approved
                                                                    by {self.env.user.employee_id.id}"""
                    group = self.env['res.groups'].search([('name', '=', 'ter_notify_employee')], limit=1)
                    self.send_notification(rec, group, notification_subject, notification_body)
                else:
                    raise ValidationError(_('Please enter valid dates.'))

            else:
                raise ValidationError("You Don't Have Access")

            return self.return_tree()

    @api.onchange('employee_id')
    @api.depends('employee_id')
    def onchange_employee_id(self):
        for rec in self:
            payslip_ids = self.env['hr.payslip'].search([('employee_id', '=', rec.employee_id.id)])
            if len(payslip_ids) != 0:
                rec.payslip_ids = payslip_ids[0]
            else:
                rec.payslip_ids = payslip_ids
            equ_ids = self.env['maintenance.equipment'].search([('employee_id', '=', rec.employee_id.id)])
            rec.equipment_ids = equ_ids

    def action_reject(self):
        return {
            'name': 'Reject EOS',
            'type': 'ir.actions.act_window',
            'res_model': 'reject.termination.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('employee_termination.view_reject_termination_wizard').id,
            'target': 'new',
        }

    def action_approve(self):
        return {
            'name': 'Approve EOS',
            'type': 'ir.actions.act_window',
            'res_model': 'approve.termination.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('employee_termination.view_approve_termination_wizard').id,
            'target': 'new',
            'context': {'default_message_label': self._compute_message_label()},
        }

    def action_print_report(self):
        return self.env.ref('employee_termination.employee_termination_report_temp').report_action(self)

    def is_employee_same_as_user(self):
        for rec in self:
            return rec.employee_id.id == self.env.user.employee_id.id

    @api.depends('payslip_ids')
    def _compute_payslip_info(self):
        for rec in self:
            if rec.payslip_ids:
                payslip = rec.payslip_ids[0]  # Assuming there's only one payslip per employee, adjust if needed
                rec.net_wage = payslip.net_wage
                rec.basic_wage = payslip.basic_wage
                rec.date_from = payslip.date_from
                rec.reference = payslip.number
                rec.payslip_run_id = payslip.payslip_run_id.id

    # @api.depends('equipment_ids')
    # def _compute_equipment_info(self):
    #     for rec in self:
    #         if rec.equipment_ids:
    #             equ = rec.equipment_ids
    #             rec.equ_name = equ.name
    #             rec.equ_assign_date = equ.assign_date
    #             rec.equ_cost = equ.cost
    #             rec.equ_effective_date = equ.effective_date

    @api.model
    def create(self, vals):
        self = self.sudo()
        # assigning the sequence for the record
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('employee.termination') or _('New')

        res = super(EmployeeTermination, self).create(vals)
        return res

    @api.onchange('employee_id')
    @api.depends('employee_id')
    def check_request_existence(self):
        self = self.sudo()
        # Check whether any resignation request already exists
        for rec in self:
            if rec.employee_id:
                resignation_request = self.env['employee.termination'].search([('employee_id', '=', rec.employee_id.id),
                                                                               (
                                                                                   'state', 'in',
                                                                                   ['submitted', 'init_manager',
                                                                                    'approved'])])
                if resignation_request:
                    raise ValidationError(_('There is a resignation request in confirmed or'
                                            ' approved state for this employee'))
                if rec.employee_id:
                    no_of_contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
                    for contracts in no_of_contract:
                        if contracts.state == 'open' and len(contracts) != 0:
                            rec.employee_contract = contracts.name
                            rec.start_date = contracts.date_start
                        else:
                            rec.employee_contract = ""
                            rec.start_date = ""

    @api.depends('resignation_type')
    @api.onchange('resignation_type')
    def _compute_employee_id_readonly(self):
        for rec in self:
            if rec.resignation_type == 'resigned':
                if self.env.user.has_group("employee_termination.ter_hr_group") or self.env.user.has_group(
                        "employee_termination.ter_hr_employee_group"):
                    rec.employee_id_readonly = False
                else:
                    rec.employee_id = False
                    rec.employee_id = self.env.user.employee_id.id
                    rec.employee_id_readonly = True
            else:
                rec.employee_id_readonly = False

    @api.depends('state', 'manager_id')
    def _compute_end_date_readonly(self):
        for rec in self:
            if rec.state == 'draft':
                rec.end_date_readonly = False
            elif rec.state == "submitted" and self.env.user.employee_id == rec.manager_id:
                rec.end_date_readonly = False
            else:
                rec.end_date_readonly = True

    def send_notification(self, rec, group_users, notification_subject, notification_body):
        for user in group_users:
            user_partner = user.partner_id
            if user_partner:
                rec.message_notify(
                    partner_ids=[user_partner.id],
                    subject=notification_subject,
                    body=notification_body,
                )

                activity_type_id = self.env['mail.activity.type'].search(
                    [('name', '=', 'EOS Request')],
                    limit=1)
                rec.activity_schedule(
                    activity_type_id=activity_type_id.id,
                    summary="EOS Request",
                    note=notification_body,
                    user_id=user.id,
                )


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    employee_termination_id = fields.Many2one('employee.termination', string="Employee Termination")


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    employee_termination_id = fields.Many2one('employee.termination', string="Employee Termination")
