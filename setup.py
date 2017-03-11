"""A setuptools based setup module.
"""
import setuptools
# To use a consistent encoding
import codecs
import os

__author__ = 'Tomasz J. Kotarba <tomasz@kotarba.net>'
__copyright__ = 'Copyright (c) 2016, Tomasz J. Kotarba. All rights reserved.'
__maintainer__ = 'Tomasz J. Kotarba'
__email__ = 'tomasz@kotarba.net'


here = os.path.abspath(os.path.dirname(__file__))


install_requires = [
    'rapidpro-python>=1.0,<=2.1.5',
    'rapidsms>=0.18.0',
    'django>=1.7,<1.9'  # rapidsms incompatible with 1.9 at the time
]


tests_require = [
    'mock',
]


# Get the long description from the README.rst file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='rapidpro-for-rapidsms',

    version='1.0.2',

    description='A RapidPro backend for RapidSMS.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/system7ltd/rapidpro-for-rapidsms',

    # Author details
    author='Tomasz J. Kotarba',
    author_email='tomasz@kotarba.net',

    license='BSD',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',

        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',

        'Framework :: Django',

        'Operating System :: OS Independent',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='rapidsms rapidpro sms django textit',

    # packages=setuptools.find_packages(exclude=['tests']),
    packages=setuptools.find_packages(),

    install_requires=install_requires,

    tests_require=tests_require,

    test_suite='run_tests.main',

    extras_require={'development': tests_require},
)
