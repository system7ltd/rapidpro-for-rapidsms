from rapidpro4rapidsms.outgoing import RapidProBackend

from mock import patch, Mock

from django.test import TestCase

from rapidsms.tests.harness import CreateDataMixin

from base import *


__author__ = 'Tomasz J. Kotarba <tomasz@kotarba.net>'
__copyright__ = 'Copyright (c) 2015, Tomasz J. Kotarba. All rights reserved.'
__maintainer__ = 'Tomasz J. Kotarba'
__email__ = 'tomasz@kotarba.net'


class RapidProSendTest(CreateDataMixin, TestCase):
    def setUp(self):
        self.mo_sms_valid_data = mo_sms_valid_data
        self.mt_sent_valid_data = mt_sent_valid_data
        self.mt_dlvd_valid_data = mt_dlvd_valid_data
        self.config = {
            'rapidpro_api_gateway_url': 'https://some.rapidpro.io/api/v1',
            'rapidpro_api_token': 'some-rapidpro-api-token'
        }

    def test_required_fields(self):
        """RapidPro backend requires the RapidPro API URL and API token in its
        configuration.
        """
        self.assertRaises(
            TypeError, RapidProBackend,
        )
        self.assertRaises(
            TypeError, RapidProBackend,
            router=None, name='rapidpro-backend',
            rapidpro_api_gateway_url='',
        )
        self.assertRaises(
            TypeError, RapidProBackend,
            router=None, name='rapidpro-backend',
            rapidpro_api_token=''
        )
        try:
            RapidProBackend(
                router=None, name='rapidpro-backend',
                rapidpro_api_gateway_url='',
                rapidpro_api_token=''
            )
        except TypeError:
            self.fail(
                'This test should not fail when all required keys are '
                'present!'
            )

    def test_rapidpro_api_token_and_gateway_url_passed_to_temba_client(self):
        """RapidPro requires all API calls to authenticate by including an
        Authorization header with a RapidPro API token. For security reasons
        all calls must be made using HTTPS.  We use temba.TembaClient (which is
        an external component created by the developer of RapidPro) to take
        care of that which means that its constructor should be called with two
        arguments - rapidpro_api_gateway_url and rapidpro_api_token - when
        method RapidProBackend._prepare_rapidpro_client() is executed.
        """
        backend = RapidProBackend(None, 'rapidpro-backend', **self.config)
        with patch(
                'temba_client.client.TembaClient.__init__',
                Mock(return_value=None)
        ) as mock_temba_constructor:
            backend._prepare_rapidpro_client()
        mock_temba_constructor.assert_called_once_with(
            self.config['rapidpro_api_gateway_url'],
            self.config['rapidpro_api_token']
        )

    def test_outgoing_keys_or_keyword_arguments_for_temba(self):
        """RapidPro requires JSON to include 'text' and at least one of:
            - urns
            - contacts
            - groups
        The current implementation supports just urns and uses class
        temba.TembaClient to authenticate with RapidPro servers and send SMS.
        We use method RapidProBackend.prepare_request() to prepare arguments
        for both the constructor of TembaClient and its method create_broadcast.
        """
        message = self.create_outgoing_message()
        backend = RapidProBackend(None, 'rapidpro-backend', **self.config)
        kwargs = backend.prepare_request(
            message.id,
            message.text,
            [message.connections[0].identity],
            {}
        )
        self.assertEqual(
            kwargs['rapidpro_api_gateway_url'],
            self.config['rapidpro_api_gateway_url']
        )
        self.assertEqual(
            kwargs['rapidpro_api_token'],
            self.config['rapidpro_api_token']
        )
        self.assertEqual(
            kwargs['urns'],
            ['tel:' + message.connections[0].identity])
        self.assertEqual(kwargs['text'], message.text)

    def test_send(self):
        """Test successful send."""
        message = self.create_outgoing_message()
        backend = RapidProBackend(None, 'rapidpro-backend', **self.config)
        kwargs = backend.prepare_request(
            message.id,
            message.text,
            [message.connections[0].identity],
            {}
        )
        with patch(
                'temba_client.client.TembaClient.create_broadcast'
        ) as mock_create_bcast:
            backend.send(
                message.id,
                message.text,
                [message.connections[0].identity],
                {}
            )
        mock_create_bcast.assert_called_once_with(
            text=kwargs['text'],
            urns=kwargs['urns']
        )
