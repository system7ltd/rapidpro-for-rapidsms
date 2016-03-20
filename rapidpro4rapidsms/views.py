import json

import logging

from rapidsms.backends.http.views import BaseHttpBackendView

from rapidpro4rapidsms.forms import RapidProForm


__author__ = 'Tomasz J. Kotarba <tomasz@kotarba.net>'
__copyright__ = 'Copyright (c) 2015, Tomasz J. Kotarba. All rights reserved.'
__maintainer__ = 'Tomasz J. Kotarba'
__email__ = 'tomasz@kotarba.net'


logger = logging.getLogger(__name__)


class RapidProBackendView(BaseHttpBackendView):
    """Backend view for handling inbound SMSes from RapidPro
    (http://rapidpro.io/)
    """
    form_class = RapidProForm
    http_method_names = ['post']
    params = {
        'identity_name': 'phone',
        'text_name': 'text',
    }

    def get_form_kwargs(self):
        kwargs = super(RapidProBackendView, self).get_form_kwargs()
        try:
            kwargs['data'] = json.loads(self.request.body)
        except ValueError:
            logger.exception("Failed to parse JSON from RapidPro.")
        return kwargs
