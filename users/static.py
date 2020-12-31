STRIPE_STATUS = ((0, 'Active'), (1, 'Pending'),
                 (2, 'Rejected'), (3, 'Restricted'), (4, 'Null'))
STRIPE_STATUS_DICT = dict((v, k) for k, v in STRIPE_STATUS)
