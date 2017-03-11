import logging

from temba_client.v1 import TembaClient

from rapidsms.backends.base import BackendBase


__author__ = 'Tomasz J. Kotarba <tomasz@kotarba.net>'
__copyright__ = 'Copyright (c) 2015, Tomasz J. Kotarba. All rights reserved.'
__maintainer__ = 'Tomasz J. Kotarba'
__email__ = 'tomasz@kotarba.net'


logger = logging.getLogger(__name__)


class RapidProBackend(BackendBase):
    """Outgoing SMS backend for RapidPro (http://rapidpro.io).  It uses method
    TembaClient.create_broadcast() to send sms.  This version does not
    support RapidPro's contacts and groups - it only uses URNs.
    """

    def configure(self, rapidpro_api_gateway_url, rapidpro_api_token, **kwargs):
        self.rapidpro_api_gateway_url = rapidpro_api_gateway_url
        if self.rapidpro_api_gateway_url is None:
            raise ValueError('No valid rapidpro_api_gateway_url set.')
        self.rapidpro_api_token = rapidpro_api_token
        if self.rapidpro_api_token is None:
            raise ValueError('No valid rapidpro_api_token set.')

    def prepare_request(self, id_, text, identities, context):
        kwargs = {
            'rapidpro_api_gateway_url': self.rapidpro_api_gateway_url,
            'rapidpro_api_token': self.rapidpro_api_token, 'text': text,
            'urns': ['tel:{}'.format(i) for i in identities]
        }
        return kwargs

    def send(self, id_, text, identities, context=None):
        """Backend sending logic. The router will call this method for each
        outbound message.
        This backend sends SMS via the configured RapidPro service using the
        TembaClient.create_broadcast(). Any exceptions raised here will
        be captured and logged by the selected router.

        If multiple ``identities`` are provided, the message is intended for
        all recipients.  The identities are translated into URNs - this version
        does not support RapidPro's contacts and groups.

        :param id_: Message ID
        :param text: Message text
        :param identities: List of identities
        :param context: Optional extra context provided by router to backend
        """
        context = context or {}
        logger.debug('Sending message: {}'.format(text))
        kwargs = self.prepare_request(id_, text, identities, context)
        client = self._prepare_rapidpro_client()
        client.create_broadcast(
            text=kwargs['text'],
            urns=kwargs['urns']
        )

    def _prepare_rapidpro_client(
            self,
            rapidpro_api_gateway_url=None,
            rapidpro_api_token=None
    ):
        if rapidpro_api_gateway_url is None:
            rapidpro_api_gateway_url = self.rapidpro_api_gateway_url
        if rapidpro_api_token is None:
            rapidpro_api_token = self.rapidpro_api_token

        client = TembaClient(
            rapidpro_api_gateway_url,
            rapidpro_api_token
        )
        return client
