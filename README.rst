rapidpro-for-rapidsms
=====================

This is the `RapidPro`_ backend for `RapidSMS`_.  It has been created for `UNICEF`_ to facilitate transition of legacy applications designed for `RapidSMS`_ and the `Django`_ web framework to the new `RapidPro`_ platform.
This component uses the official `rapidpro-python`_ client library to communicate with RapidPro.

Features
--------

* Incoming (MO) SMS support
* Outgoing (MT) SMS support
* New configuration options
    * RapidPro API gateway URL
    * RapidPro API token

Requirements
------------

* Python 2.7+ or Python 3.3+
* Django >=1.7,<=1.9
* RapidSMS 0.18.0+
* rapidpro-python >=1.0,<=2.1.5

Installation
------------

The rapidpro-for-rapidsms backend supports Python >= 2.7 and Django >= 1.7.  All required Python packages should be intalled automatically as long as you follow the official installation procedure described below.

To install from PyPi::

    $ pip install rapidpro-for-rapidsms

Configuration
-------------

Edit your Django project settings (e.g. ``settings.py``) to include the following:

* add ``rapidpro4rapidsms`` to your ``INSTALLED_APPS``, e.g.::

    INSTALLED_APPS = (
        # your apps
        'rapidpro4rapidsms',
    )

* configure the backend to use your RapidPro service and API token, e.g.::

    INSTALLED_BACKENDS = {
        # some other backends (optional)
        "rapidpro-backend": {
            "ENGINE": "rapidpro4rapidsms.RapidProBackend",
            # The following URL and token should be set to match your RapidPro
            "rapidpro_api_gateway_url": "your rapidpro API gateway URL, e.g. "
                                                "http://127.0.0.1:8080/api/v1"
                                                "or"
                                                "rapidpro.io",
            "rapidpro_api_token": "YOUR-RAPIDPRO-API-TOKEN"
        }
    } 
 

* configure your Django project to include rapidpro4rapidsms.urls, e.g.::

    urlpatterns = patterns(
        # your Django project URLs
        # ...
        # rapidpro4rapidsms URLs
        url(r'backends/', include('rapidpro4rapidsms.urls')),
    )

LICENSE
-------

The rapidpro-for-rapidsms backend is released under the BSD License. See the  `LICENSE.TXT`_ file for more details.

Development
-----------

To install::

    $ pip install -e .[development]

To run tests::

    $ python setup.py test

Contributing
------------

If you think you've found a bug or are interested in contributing to this
project check out `rapidpro-for-rapidsms on Github <https://github.com/system7ltd/rapidpro-for-rapidsms>`_.

Development by Tomasz J. Kotarba of `SYSTEM7 <http://system7.IT>`_.

.. _RapidSMS: http://www.rapidsms.org/
.. _RapidPro: http://www.rapidpro.io/
.. _rapidpro-python: http://pypi.python.org/pypi/rapidpro-python
.. _UNICEF: http://www.unicef.org/
.. _Django: https://www.djangoproject.com/
.. _LICENSE.TXT: http://github.com/system7ltd/rapidpro-for-rapidsms/blob/master/LICENSE.txt
