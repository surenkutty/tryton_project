from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction

__metaclass__ = PoolMeta

STATES = {
    'readonly': ~fields.Eval('state') == 'draft',
}

class CustomerOrder(ModelSQL, ModelView):
    'Customer Order'
    __name__ = 'customer.order'

    customer = fields.Many2One('party.party', 'Customer', required=True, states=STATES)
    order_date = fields.Date('Order Date', required=True, states=STATES)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], 'State', required=True, readonly=True)

    lines = fields.One2Many('customer.order.line', 'order', 'Order Lines')
    total_amount = fields.Function(fields.Numeric('Total'), 'get_total')

    def get_total(self, name):
        return sum(l.subtotal for l in self.lines)

    @classmethod
    def __setup__(cls):
        super(CustomerOrder, cls).__setup__()
        cls._transitions.update({
            ('draft', 'confirmed'),
            ('confirmed', 'done'),
        })

    @classmethod
    def confirm(cls, orders):
        cls.write(orders, {'state': 'confirmed'})

    @classmethod
    def process(cls, orders):
        cls.write(orders, {'state': 'done'})
