# -*- coding: utf-8 -*-
from contextlib import contextmanager, nested
from django.conf import settings
try:
    from django.conf.urls.defaults import patterns, url, include
except ImportError:
    from django.conf.urls import patterns, url, include  # pragma: no cover
from django.core.management.base import BaseCommand
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.test.client import Client


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


def make_static(template, language, request={}):
    with nested(override_urlconf(), override_middleware()):
        client = Client()
        client.cookies['django_language'] = language
        request.update({'template':template})
        response = client.get('/', request)
        if response.status_code != 200:
            raise InvalidResponseError(
                'Response code was %d, expected 200' % response.status_code
            )
        return response.content


class Command(BaseCommand):
    def handle(self, template, language="en", extra_request=None, **options):
        request = {}
        try:
            if extra_request:
                for var in extra_request.split(","):
                    request[var.split("=")[0]] = var.split("=")[1]
        except:
            raise ValueError("error in extra_request parameter: syntax variable=value,variable=value")
        output = make_static(template, language, request)
        self.stdout.write(output)


def render(request):
    template_name = request.GET['template']
    return render_to_response(template_name, RequestContext(request))


urlpatterns = patterns('',
    url('^$', render),
    url('^others', include(settings.ROOT_URLCONF))
)
