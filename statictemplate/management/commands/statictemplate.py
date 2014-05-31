# -*- coding: utf-8 -*-
from contextlib import contextmanager, nested
from optparse import make_option
import urlparse

from django.conf import settings
try:
    from django.conf.urls.defaults import patterns, url, include
except ImportError:  # pragma: no cover
    from django.conf.urls import patterns, url, include  # pragma: no cover
from django.core.management.base import BaseCommand
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.test.client import Client
try:
    from django.utils.encoding import force_text
except ImportError:  # pragma: no cover
    from django.utils.encoding import force_unicode as force_text  # pragma: no cover
from django.utils.translation import get_language


class InvalidResponseError(Exception):
    pass


@contextmanager
def override_urlconf():
    has_old = hasattr(settings, 'ROOT_URLCONF')
    old = getattr(settings, 'ROOT_URLCONF', None)
    settings.ROOT_URLCONF = 'statictemplate.management.commands.statictemplate'
    yield
    if has_old:
        setattr(settings, 'ROOT_URLCONF', old)
    else:  # pragma: no cover
        delattr(settings, 'ROOT_URLCONF')


@contextmanager
def override_middleware():
    has_old = hasattr(settings, 'MIDDLEWARE_CLASSES')
    old = getattr(settings, 'MIDDLEWARE_CLASSES', None)
    settings.MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    )
    yield
    if has_old:
        setattr(settings, 'MIDDLEWARE_CLASSES', old)
    else:  # pragma: no cover
        delattr(settings, 'MIDDLEWARE_CLASSES')


def make_static(template, language=None, request=None):
    with nested(override_urlconf(), override_middleware()):
        client = Client()
        if not request:
            request = {}
        if language:
            client.cookies['django_language'] = language
        request.update({'template': template})
        response = client.get('/', request)
        if response.status_code != 200:
            raise InvalidResponseError(  # pragma: no cover
                'Response code was %d, expected 200' % response.status_code
            )
        return response.content


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--file', '-f',
                    action='store',
                    dest='output',
                    help='Output file'),
        )

    def handle(self, template, language=None, extra_request=None, **options):
        request = {}
        if not language:
            language = get_language()
        if extra_request:
            request.update(urlparse.parse_qs(extra_request, strict_parsing=True))
        output = make_static(template, language, request)
        if options.get('output', False):
            with open(options.get('output'), 'w') as output_file:
                output_file.write(output)
        else:
            self.stdout.write(force_text(output))


def render(request):
    template_name = request.GET['template']
    return render_to_response(template_name, RequestContext(request))


urlpatterns = patterns('',
    url('^$', render),
    url('^', include(settings.ROOT_URLCONF))
)