from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta

__metaclass__ = PoolMeta

class CustomerOrderLine(ModelSQL, ModelView):
    'Customer Order Line'
    __name__ = 'customer.order.line'

    order = fields.Many2One('customer.order', 'Order', required=True, ondelete='CASCADE')
    product = fields.Many2One('product.product', 'Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    unit_price = fields.Numeric('Unit Price', required=True)
    subtotal = fields.Function(fields.Numeric('Subtotal'), 'get_subtotal')

    def get_subtotal(self, name):
        return self.quantity * self.unit_price
