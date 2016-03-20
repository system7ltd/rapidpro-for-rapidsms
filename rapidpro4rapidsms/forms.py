from django import forms
from django.forms.utils import ErrorList

from rapidsms.backends.http.forms import BaseHttpForm


__author__ = 'Tomasz J. Kotarba <tomasz@kotarba.net>'
__copyright__ = 'Copyright (c) 2015, Tomasz J. Kotarba. All rights reserved.'
__maintainer__ = 'Tomasz J. Kotarba'
__email__ = 'tomasz@kotarba.net'


class RapidProForm(BaseHttpForm):
    SUPPORTED_EVENT_CODES = ['mo_sms', 'mt_sent', 'mt_dlvd']

    # Fields required irrespective of the event type:
    event = forms.CharField()
    sms = forms.IntegerField()  # message id
    relayer_phone = forms.CharField()
    phone = forms.CharField()
    text = forms.CharField()
    time = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S.%f'])

    # Fields required for some events and optional for others:
    # The channel field is currently required for the mo_sms event.
    channel = forms.IntegerField(required=False)
    # The relayer field is currently required for both mt_* events.
    relayer = forms.IntegerField(required=False)

    def _add_error_message(self, field_name, message):
        if field_name not in self._errors:
            self._errors[field_name] = ErrorList([message])
        else:
            self._errors[field_name].append(message)

    def clean(self):
        field_required_error = 'This field is required.'
        event = self.cleaned_data.get('event', None)
        if event not in self.SUPPORTED_EVENT_CODES:
            self._add_error_message(
                'event',
                'The event code must be one of: {}.'.format(
                    ', '.join((s for s in self.SUPPORTED_EVENT_CODES))
                )
            )
        elif event == 'mo_sms':
            if not self.cleaned_data.get('channel', None):
                self._add_error_message('channel', field_required_error)
        # Both mt_sent and mt_dlvd have the same fields in the current version
        # of RapidPro.
        elif event[:3] == 'mt_':
            if not self.cleaned_data.get('relayer', None):
                self._add_error_message('relayer', field_required_error)
        return self.cleaned_data

    def get_incoming_data(self):
        connections = self.lookup_connections([self.cleaned_data['phone']])
        return {
            'connection': connections[0],
            'text': self.cleaned_data['text'],
        }
