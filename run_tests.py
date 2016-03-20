#!/usr/bin/env python

import os
import sys
import optparse

import django
import django.conf
import django.test.utils


__author__ = 'Tomasz J. Kotarba <tomasz@kotarba.net>'
__copyright__ = 'Copyright (c) 2016, Tomasz J. Kotarba. All rights reserved.'
__maintainer__ = 'Tomasz J. Kotarba'
__email__ = 'tomasz@kotarba.net'


def parse_command_line_arguments():
    usage = "%prog [options] [module module module ...]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-v', '--verbosity', action='store', dest='verbosity',
                      default=1, type='choice', choices=['0', '1', '2', '3'],
                      help='Verbosity level; 0=minimal output, 1=normal '
                           'output, 2=all output')
    parser.add_option('--noinput', action='store_false', dest='interactive',
                      default=True,
                      help='Tells Django to NOT prompt the user for input of '
                           'any kind.')
    parser.add_option('--settings',
                      help='Python path to settings module, e.g. '
                           '"myproject.settings". If this isn\'t provided, '
                           'the DJANGO_SETTINGS_MODULE environment variable '
                           'will be used.')
    options, arguments = parser.parse_args()
    if options.settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
    elif "DJANGO_SETTINGS_MODULE" in os.environ:
        options.settings = os.environ['DJANGO_SETTINGS_MODULE']
    return options, arguments


def configure_django_settings():
    django.conf.settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'rapidsms',
            'rapidpro4rapidsms',
        ),
        SITE_ID=1,
        SECRET_KEY='the-password',
        LOGGING={
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'null': {
                    'level': 'DEBUG',
                    'class': 'django.utils.log.NullHandler',
                },
            },
            'loggers': {
                'rapidsms': {
                    'handlers': ['null'],
                    'level': 'DEBUG',
                },
                'rapidpro4rapidsms': {
                    'handlers': ['null'],
                    'level': 'DEBUG',
                }
            }
        },
        ROOT_URLCONF='rapidpro4rapidsms.urls',
        INSTALLED_BACKENDS={
            "rapidpro-backend": {
                "ENGINE": "rapidpro4rapidsms.RapidProBackend",
                "rapidpro_api_gateway_url": "http://127.0.0.1:8080/api/v1",
                "rapidpro_api_token": "YOUR-RAPIDPRO-API-TOKEN"
            }
        }
    )


def prepare_django_test_runner(options):
    if not options.settings:
        configure_django_settings()
    if django.VERSION > (1, 7):
        # django.readthedocs.org/en/latest/releases/1.7.html#standalone-scripts
        django.setup()
    test_runner_class = django.test.utils.get_runner(django.conf.settings)
    test_runner = test_runner_class(verbosity=int(options.verbosity),
                                    interactive=options.interactive,
                                    failfast=False)
    return test_runner


def run_tests(test_runner, arguments):
    if not arguments or arguments[0] == 'test':
        arguments = ['tests']
    failures = test_runner.run_tests(arguments)
    sys.exit(failures)


def main():
    options, arguments = parse_command_line_arguments()
    test_runner = prepare_django_test_runner(options)
    run_tests(test_runner, arguments)


if __name__ == '__main__':
    main()
