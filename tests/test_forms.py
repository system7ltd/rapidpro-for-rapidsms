from django.test import TestCase

from rapidpro4rapidsms.forms import RapidProForm

from base import *


__author__ = 'Tomasz J. Kotarba <tomasz@kotarba.net>'
__copyright__ = 'Copyright (c) 2015, Tomasz J. Kotarba. All rights reserved.'
__maintainer__ = 'Tomasz J. Kotarba'
__email__ = 'tomasz@kotarba.net'


class RapidProFormTest(TestCase):
    def setUp(self):
        self.mo_sms_valid_data = mo_sms_valid_data
        self.mt_sent_valid_data = mt_sent_valid_data
        self.mt_dlvd_valid_data = mt_dlvd_valid_data

    def test_valid_mo_sms_form_get(self):
        """Form should be valid if all required POST keys for mo_sms match
        configuration.
        """
        form = RapidProForm(
            self.mo_sms_valid_data,
            backend_name='rapidpro-backend'
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_mt_sent_form_get(self):
        """Form should be valid if all required POST keys for mt_sent match
        configuration.
        """
        form = RapidProForm(
            self.mt_sent_valid_data,
            backend_name='rapidpro-backend'
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_mt_dlvd_form_get(self):
        """Form should be valid if all required POST keys for mt_dlvd match
        configuration.
        """
        form = RapidProForm(
            self.mt_dlvd_valid_data,
            backend_name='rapidpro-backend'
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_mo_sms_form_without_channel_or_relayer_phone_invalid(self):
        """Form is invalid if channel or relayer_phone keys not present.
        """
        data = copy.copy(self.mo_sms_valid_data)
        del data['channel']
        del data['relayer_phone']
        form = RapidProForm(data, backend_name='rapidpro-backend')
        self.assertFalse(form.is_valid())

    def test_mt_sent_form_without_relayer_or_relayer_phone_invalid(self):
        """Form is invalid if relayer or relayer_phone keys not present.
        """
        data = copy.copy(self.mt_sent_valid_data)
        del data['relayer']
        del data['relayer_phone']
        form = RapidProForm(data, backend_name='rapidpro-backend')
        self.assertFalse(form.is_valid())

    def test_mt_dlvd_form_without_relayer_or_relayer_phone_invalid(self):
        """Form is invalid if relayer or relayer_phone keys not present.
        """
        data = copy.copy(self.mt_dlvd_valid_data)
        del data['relayer']
        del data['relayer_phone']
        form = RapidProForm(data, backend_name='rapidpro-backend')
        self.assertFalse(form.is_valid(), form.errors)

    def test_form_without_supported_event_code_invalid(self):
        """Form is invalid if the event code unsupported or not present.
        """
        data = copy.copy(self.mo_sms_valid_data)
        data['event'] = 'invalid_event_code'
        form = RapidProForm(data, backend_name='rapidpro-backend')
        self.assertRegexpMatches(
            str(form.errors),
            r'.*The event code must be one of: .*'
        )
        self.assertFalse(form.is_valid(), form.errors)

    def test_invalid_mo_sms_form_post(self):
        """Form is invalid if required POST keys not present.
        """
        data = {
            'event': 'mo_sms',
            'invalid-phone': '1112223333',
        }
        form = RapidProForm(data, backend_name='rapidpro-backend')
        self.assertFalse(form.is_valid(), form.errors)

    def test_invalid_mt_sent_form_post(self):
        """Form is invalid if required POST keys not present.
        """
        data = {
            'event': 'mt_sent',
            'invalid-phone': '1112223333',
        }
        form = RapidProForm(data, backend_name='rapidpro-backend')
        self.assertFalse(form.is_valid())

    def test_invalid_mt_dlvd_form_post(self):
        """Form is invalid if required POST keys not present.
        """
        data = {
            'event': 'mt_dlvd',
            'invalid-phone': '1112223333',
        }
        form = RapidProForm(data, backend_name='rapidpro-backend')
        self.assertFalse(form.is_valid())

    def test_get_incoming_data_for_mo_sms(self):
        """Method get_incoming_data should return matching text and connection
        for a valid mo_sms event form.
        """
        form = RapidProForm(
            self.mo_sms_valid_data,
            backend_name='rapidpro-backend'
        )
        form.is_valid()
        incoming_data = form.get_incoming_data()
        self.assertEqual(
            self.mo_sms_valid_data['text'],
            incoming_data['text']
        )
        self.assertEqual(
            self.mo_sms_valid_data['phone'],
            incoming_data['connection'].identity
        )
        self.assertEqual(
            'rapidpro-backend',
            incoming_data['connection'].backend.name
        )

    def test_get_incoming_data_for_mt_sent(self):
        """Method get_incoming_data should return matching text and connection
        for a valid mo_sent event form.
        """
        form = RapidProForm(
            self.mt_sent_valid_data,
            backend_name='rapidpro-backend'
        )
        form.is_valid()
        incoming_data = form.get_incoming_data()
        self.assertEqual(
            self.mo_sms_valid_data['text'],
            incoming_data['text']
        )
        self.assertEqual(
            self.mo_sms_valid_data['phone'],
            incoming_data['connection'].identity
        )
        self.assertEqual(
            'rapidpro-backend',
            incoming_data['connection'].backend.name
        )

    def test_get_incoming_data_for_mt_dlvd(self):
        """Method get_incoming_data should return matching text and connection
        for a valid mt_dlvd event form.
        """
        form = RapidProForm(
            self.mt_dlvd_valid_data,
            backend_name='rapidpro-backend'
        )
        form.is_valid()
        incoming_data = form.get_incoming_data()
        self.assertEqual(
            self.mo_sms_valid_data['text'],
            incoming_data['text']
        )
        self.assertEqual(
            self.mo_sms_valid_data['phone'],
            incoming_data['connection'].identity
        )
        self.assertEqual(
            'rapidpro-backend',
            incoming_data['connection'].backend.name
        )
