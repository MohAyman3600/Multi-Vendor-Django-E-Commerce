"""Static variables."""

# Ordered: We’ve gotten your order and are preparing to send it.
#  You still might be able to cancel the order.
# Shipped: The shipping company has shipped your order.
# Delivered: The shipping company has delivered your order.
# Unable to deliver: The shipping provider wasn’t able to deliver your order,
#  and it has been returned. Contact support to get a refund.
#  It might take several days for your refund to appear on your statement,
#  depending on your bank.
# Canceled: The order has been canceled.
ORDER_STATUS = ((0, 'Ordered'), (1, 'Shipped'),
                (2, 'Delivered'), (3, 'Unable to deliver'), (4, 'Canceled'))
ORDER_STATUS_DICT = dict((v, k) for k, v in ORDER_STATUS)

PRODUCT_PAYMENT_STATUS = ((0, 'error'), (1, 'success'), (2, 'pending'))
PRODUCT_PAYMENT_STATUS_DICT = dict((v, k) for k, v in PRODUCT_PAYMENT_STATUS)
