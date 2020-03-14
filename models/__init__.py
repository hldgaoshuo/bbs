import time
import os

import secret

from marrow.mailer import Mailer


def current_time():
    return int(time.time())


def configured_mailer():
    config = {
        'transport.debug': True,
        'transport.timeout': 1,
        'transport.use': 'smtp',
        'transport.host': 'smtp.exmail.qq.com',
        'transport.port': 465,
        'transport.tls': 'ssl',
        'transport.username': os.environ['ADMIN_MAIL'],
        'transport.password': secret.mail_password,
    }
    m = Mailer(config)
    m.start()
    return m


mailer = configured_mailer()
