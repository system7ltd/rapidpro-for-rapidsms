import copy


__author__ = 'Tomasz J. Kotarba <tomasz@kotarba.net>'
__copyright__ = 'Copyright (c) 2015, Tomasz J. Kotarba. All rights reserved.'
__maintainer__ = 'Tomasz J. Kotarba'
__email__ = 'tomasz@kotarba.net'


_common_data = {
    'event': None,
    'sms': 23554,
    'relayer_phone': '%2B250788111111',
    'phone': '%2B250788123123',
    'text': 'This+is+a+test+message.',
    'time': '2013-01-01T05:34:34.034'
}


mo_sms_valid_data = copy.copy(_common_data)
mo_sms_valid_data['event'] = 'mo_sms'
mo_sms_valid_data['channel'] = 254


mt_sent_valid_data = copy.copy(_common_data)
mt_sent_valid_data['event'] = 'mt_sent'
mt_sent_valid_data['relayer'] = 254


mt_dlvd_valid_data = copy.copy(mt_sent_valid_data)
mt_dlvd_valid_data['event'] = 'mt_dlvd'
