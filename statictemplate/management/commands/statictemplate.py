# -*- coding: utf-8 -*-
from contextlib import contextmanager
from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.core.management.base import BaseCommand
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.test.client import Client

@contextmanager
def override_urlconf():
    has_old = hasattr(settings, 'ROOT_URLCONF')
    old = getattr(settings, 'ROOT_URLCONF', None)
    settings.ROOT_URLCONF = 'statictemplate.management.commands.statictemplate'
    yield
    if has_old:
        setattr(settings, 'ROOT_URLCONF', old)
    else: # pragma: no cover
        delattr(settings, 'ROOT_URLCONF')

def make_static(template):
    with override_urlconf():
        client = Client()
        response = client.get('/', {'template': template})
        return response.content


class Command(BaseCommand):
    def handle(self, template, **options):
        output = make_static(template)
        self.stdout.write(output)


def render(request):
    template_name = request.GET['template']
    return render_to_response(template_name, RequestContext(request))


urlpatterns = patterns('',
    url('^$', render),
    url('^others', include(settings.ROOT_URLCONF))
)
