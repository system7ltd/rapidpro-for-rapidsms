import json

from django.core.urlresolvers import reverse

from rapidsms.tests.harness import RapidTest

from base import *


__author__ = 'Tomasz J. Kotarba <tomasz@kotarba.net>'
__copyright__ = 'Copyright (c) 2015, Tomasz J. Kotarba. All rights reserved.'
__maintainer__ = 'Tomasz J. Kotarba'
__email__ = 'tomasz@kotarba.net'


class RapidProViewTest(RapidTest):
    def setUp(self):
        self.mo_sms_valid_data = mo_sms_valid_data
        self.mt_sent_valid_data = mt_sent_valid_data
        self.mt_dlvd_valid_data = mt_dlvd_valid_data
        self.http_backend_url = reverse('rapidpro-backend')

    def test_valid_response_post(self):
        """Should return HTTP 200 with valid POST data."""
        response = self.client.post(
            self.http_backend_url,
            json.dumps(self.mo_sms_valid_data),
            content_type='text/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_response_post(self):
        """Should return HTTP 400 if POST data is invalid."""
        data = {'invalid-field': '1112223333', 'another-invalid-field': '123'}
        response = self.client.post(
            self.http_backend_url,
            json.dumps(data),
            content_type='text/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        """Should return HTTP 400 if JSON is invalid."""
        data = '{this is not a valid json, , [}'
        response = self.client.post(
            self.http_backend_url, data, content_type='text/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_valid_post_message(self):
        """Valid POSTs should pass message object to router."""
        self.client.post(
            self.http_backend_url,
            json.dumps(self.mo_sms_valid_data),
            content_type='text/json'
        )
        message = self.inbound[0]
        self.assertEqual(self.mo_sms_valid_data['text'], message.text)
        self.assertEqual(
            self.mo_sms_valid_data['phone'],
            message.connection.identity
        )
        self.assertEqual(
            'rapidpro-backend',
            message.connection.backend.name
        )
