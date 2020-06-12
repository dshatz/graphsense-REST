from flask import abort, current_app

MAX_DEPTH = 7
LABEL_PREFIX_LENGTH = 3


def check_inputs(**kwargs):
    for key, value in kwargs.items():
        if key in ['address', 'tx', 'direction', 'neighbor']:
            if not isinstance(value, str) or not value.isalnum():
                abort(400, 'Invalid {}'.format(key))
        if key in ['page']:
            if value and not value.isalnum():
                abort(400, 'Invalid {}'.format(key))
        if key in ['pagesize'] and value:
            try:
                value = int(value)
            except ValueError:
                abort(400, 'Invalid {}'.format(key))
        if key in ['limit'] and value:
            try:
                value = int(value)
                return value
            except ValueError:
                abort(400, 'Invalid {}'.format(key))
        if key in ['currency_optional']:
            if value and value not in current_app.config['MAPPING']:
                abort(404, 'Unknown currency in config: {}'.format(value))
        if key in ['currency']:
            if value not in current_app.config['MAPPING']:
                abort(404, 'Unknown currency in config: {}'.format(value))
        if key in ['depth']:
            if value > MAX_DEPTH:
                abort(400, "Depth must not exceed {}".format(MAX_DEPTH))
        if key in ['category']:
            if value and not value.isalpha():
                abort(400, 'Invalid {}'.format(key))
        if key in ['label']:
            if not value:
                abort(400, "Missing {}, please specify one.".format(key))
            if len(value) < LABEL_PREFIX_LENGTH:
                abort(400, "Label parameter too short: at least {} characters"
                      .format(LABEL_PREFIX_LENGTH))
        if key in ['addresses']:
            if isinstance(value, str):
                for a in value.split(','):
                    if not a.isalnum():
                        abort(400, 'Invalid address')
        if key in ['expression']:
            if not value:
                abort(400, 'Empty search expression')
            # if invalid label and invalid tx and invalid address
            can_be_label = False
            can_be_tx_address = False
            if len(value) >= LABEL_PREFIX_LENGTH:
                can_be_label = True
            if value.isalnum():
                can_be_tx_address = True
            if not can_be_label and not can_be_tx_address:
                abort(400, 'Invalid search expression')
            return can_be_label, can_be_tx_address
        elif key in ['height', 'entity']:
            if value is None:
                abort(400, 'Invalid {}'.format(key))
