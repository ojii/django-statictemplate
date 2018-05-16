# -*- coding: utf-8 -*-
import codecs
from contextlib import contextmanager

from django.conf import settings
from django.conf.urls import include, url
from django.core.management.base import BaseCommand
from django.shortcuts import render
from django.test.client import Client
from django.utils.encoding import force_text
from django.utils.six.moves.urllib_parse import parse_qs
from django.utils.translation import get_language

try:
    from django.urls import clear_url_caches
except ImportError:
    from django.core.urlresolvers import clear_url_caches


class InvalidResponseError(Exception):
    pass


@contextmanager
def override_urlconf():
    has_old = hasattr(settings, 'ROOT_URLCONF')
    old = getattr(settings, 'ROOT_URLCONF', None)
    settings.ROOT_URLCONF = 'statictemplate.management.commands.statictemplate'
    clear_url_caches()
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
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
        )
        yield
        if has_old:
            setattr(settings, 'MIDDLEWARE_CLASSES', old)
        else:  # NOQA
            delattr(settings, 'MIDDLEWARE_CLASSES')
    else:
        yield  # pragma: no cover


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
    def add_arguments(self, parser):
        parser.add_argument('--file', '-f',
                            action='store',
                            dest='output',
                            help='Output file'),
        parser.add_argument('--extra_request', '-e',
                            action='store',
                            dest='extra_request',
                            help='Extra request parameters in urlencoded format')
        parser.add_argument('--language-code', '-l',
                            action='store',
                            dest='language_code',
                            help='Language Code')
        parser.add_argument('template', nargs='+', type=str)

    def handle(self, template, language=None, extra_request=None, **options):
        request = {}
        language_code = options.get('language_code', language)
        language = language_code or language or get_language()
        if not extra_request:
            extra_request = options.get('extra_request', [])
        if extra_request:
            request.update(parse_qs(extra_request, strict_parsing=True))
        output = make_static(template, language, request)
        if options.get('output', False):
            with codecs.open(options.get('output'), 'w', 'utf-8') as output_file:
                output_file.write(output)
        else:
            self.stdout.write(output)


def render_view(request):
    template_name = request.GET['template']
    return render(request, template_name)


urlpatterns = [
    url('^$', render_view),
    url('^', include(settings.ROOT_URLCONF))
]
