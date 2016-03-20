from django.conf.urls import url

from rapidpro4rapidsms.views import RapidProBackendView


__author__ = 'Tomasz J. Kotarba <tomasz@kotarba.net>'
__copyright__ = 'Copyright (c) 2015, Tomasz J. Kotarba. All rights reserved.'
__maintainer__ = 'Tomasz J. Kotarba'
__email__ = 'tomasz@kotarba.net'


urlpatterns = (
    url(
        r"^rapidpro/$",
        RapidProBackendView.as_view(
            backend_name='rapidpro-backend'
        ),
        name='rapidpro-backend'
    ),
)
