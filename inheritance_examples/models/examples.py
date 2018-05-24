from odoo import api,models,fields,_

class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    product_type = fields.Selection("Product Type",related='product_id.type')

class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line.product_id')
    def _get_weight(self):
        for rec in self.order_line:
            self.gross_weight += rec.product_id.weight
            print("\n\n--------gross weight===============>",self.gross_weight,rec.product_id.weight)

    @api.multi
    def action_wizard(self):
        ctx = dict(self.env.context)
        print ("\n\n context-------------------->",ctx)
        action = {
            'name': _('Open Order Line wizard'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('inheritance_examples.sale_order_line_wizard').id,
            'context': ctx,
            'target' : 'new',
        }
        return action

    gross_weight = fields.Float("Gross Weight",compute="_get_weight")
    company_type = fields.Selection("Company Type",related="partner_id.company_type")



class sale_order_wizard(models.TransientModel):
    _name='sale.order.wizard'


    product_id = fields.Many2one('product.product','Product')
    qty = fields.Float('Quantity',default=1)
    unit_price = fields.Float('Unit Price',related='product_id.list_price')

    @api.multi
    def save_order_line(self):
        for rec in self:
            active_id = rec._context.get('active_id')
            print ("\n\nActive id ==>====================>", active_id)

            order_line = self.env['sale.order.line'].create({
                'product_id': self.product_id.id,
                'product_uom_qty': self.qty,
                'price_unit': self.unit_price,
                'order_id': active_id
            })

            print ("\n\norder_line------>", order_line)