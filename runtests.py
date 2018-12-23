# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

urlpatterns = [
]

DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'statictemplate',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
        }
    },
    LANGUAGES=(
        ('en-us', 'English'),
        ('it', 'Italian'),
    ),
    ROOT_URLCONF='runtests',
    SITE_ID=1,
    MIDDLEWARE_CLASSES=[
        'django.middleware.http.ConditionalGetMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
)


def runtests():
    import django
    from django.conf import settings

    DEFAULT_SETTINGS['TEMPLATES'] = [{
        'NAME': 'django',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    }]

    # Compatibility with Django 1.7's stricter initialization
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    if hasattr(django, 'setup'):
        django.setup()

    from django.test.runner import DiscoverRunner
    test_args = ['statictemplate']
    failures = DiscoverRunner(
        verbosity=1, interactive=True, failfast=False
    ).run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
