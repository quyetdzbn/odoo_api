from AptUrl.Helpers import _

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Phe_Duyet(models.Model):
    _name = 'phe.duyet'
    _description = 'test'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    check_current_user = fields.Boolean(compute='check_user')
    name = fields.Many2one('res.partner')
    status = fields.Selection([('approve', 'Approve'), ('not_approve_yet', 'Not approve yet'),
                               ('refuse', 'Refuse approve')], default="not_approve_yet")
    point = fields.Many2one('plan.sale.order')
    check_refuse_status = fields.Boolean(compute='check_refuse')

    def check_refuse(self):
        for rec in self:
            rec.check_refuse_status = False
            if rec.point.check_status == 'refuse_approve':
                rec.check_refuse_status = True

    @api.depends('name')
    def check_user(self):
        for rec in self:
            rec.check_current_user = False
            if rec.name != self.env.user.partner_id:
                rec.check_current_user = False
            else:
                rec.check_current_user = True

    def approve_status(self):
        for rec in self:
            rec.status = 'approve'

        count = 0
        count1 = 0
        for rec1 in self.point.list_check_names:
            count1 += 1
            if rec1.status == 'approve':
                # self.point.check_status = 'duyet'
                count += 1
            elif rec1.status == 'refuse':
                self.point.check_status = 'refuse_approve'
                rec.point.message_post(body=_('failed'), partner_ids=rec.create_uid.ids)

        if count == count1:
            self.point.check_status = 'approve'
            rec.point.message_post(body=_('successful'),  message_type='email', partner_ids=rec.create_uid.partner_id.ids)


    def refuse_status(self):
        for rec in self:
            rec.status = 'refuse'
            rec.point.message_post(body=_('failed'), message_type='email', partner_ids=rec.create_uid.partner_id.ids)

            rec.point.check_status = 'refuse_approve'
