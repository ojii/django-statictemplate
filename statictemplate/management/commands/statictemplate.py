# -*- coding: utf-8 -*-
from contextlib import contextmanager
import codecs
from optparse import make_option
try:
    import urlparse
except ImportError:  # NOQA
    from urllib import parse as urlparse
from django.conf import settings
try:
    from django.conf.urls.defaults import patterns, url, include
except ImportError:  # NOQA
    from django.conf.urls import patterns, url, include
from django.core.management.base import BaseCommand
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.test.client import Client
try:
    from django.utils.encoding import force_text
except ImportError:  # NOQA
    from django.utils.encoding import force_unicode as force_text
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
    else:  # NOQA
        delattr(settings, 'ROOT_URLCONF')


@contextmanager
def override_middleware():
    from ...settings import OVERRIDE_MIDDLEWARE
    if OVERRIDE_MIDDLEWARE:
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
        else:  # NOQA
            delattr(settings, 'MIDDLEWARE_CLASSES')
    else:
        yield


def make_static(template, language=None, request=None):
    with override_urlconf():
        with override_middleware():
            client = Client()
            if not request:
                request = {}
            if language:
                client.cookies['django_language'] = language
            request.update({'template': template})
            response = client.get('/', request)
            if response.status_code != 200:
                raise InvalidResponseError(  # NOQA
                    'Response code was %d, expected 200' % response.status_code
                )
            return force_text(response.content)


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
            request.update(urlparse.parse_qs(extra_request,
                                             strict_parsing=True))
        output = make_static(template, language, request)
        if options.get('output', False):
            with codecs.open(options.get('output'), 'w', 'utf-8') as output_file:
                output_file.write(output)
        else:
            self.stdout.write(output)


def render(request):
    template_name = request.GET['template']
    return render_to_response(template_name, RequestContext(request))


urlpatterns = patterns('',
    url('^$', render),
    url('^', include(settings.ROOT_URLCONF))
)
