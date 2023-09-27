from pkg_resources import _

from odoo import models, fields, api


class OrderLimitConfiguration(models.Model):
    _name = 'order.limit.configuration'
    _description = 'new'
    link_to_b = fields.Many2many('limit_order_staff')

    def action_open_config(self):
        view_form_id = self.env.ref('purchase_custom.order_limit_configuration_view_form').id
        setting = self.env['order.limit.configuration'].search([], limit=1)

        if setting:
            res_id = setting.id
            return {
                'name': _('Order limit configuration'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'target': 'current',
                'view_id': view_form_id,
                'res_id': res_id,
                'res_model': 'order.limit.configuration',
                'context': {'create': False,'edit': True},
            }
        else:
            return {
                'name': _('Order limit configuration'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'target': 'current',
                'view_id': view_form_id,
                'res_model': 'order.limit.configuration',
                'context': {'create': False,'edit': True},
            }