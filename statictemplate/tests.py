# -*- coding: utf-8 -*-
from distutils.version import LooseVersion

import django

try:
    from StringIO import StringIO
except:
    from io import StringIO
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.management import call_command
try:
    from django.template import TemplateDoesNotExist
except:
    from django.template.base import TemplateDoesNotExist
try:
    from django.template.loaders.base import Loader
except ImportError:
    from django.template.loader import BaseLoader as Loader
from django.test import SimpleTestCase
from tempfile import mkstemp
from statictemplate.management.commands.statictemplate import make_static, \
    InvalidResponseError

from . import settings as statictemplate_settings


class TestLoader(Loader):
    is_usable = True
    templates = {
        'request': '{% extends "base" %}{% block content %}request {{ request.GET.extra }}{% endblock %}',
        'simple': '{% extends "base" %}{% block content %}simple{% endblock %}',
        'base': '{% block head %}head{% endblock %}{% block content %}content{% endblock %}',
    }

    def load_template_source(self, template_name, template_dirs=None):
        found = self.templates.get(template_name, None)
        if not found:  # pragma: no cover
            raise TemplateDoesNotExist(template_name)
        return found, template_name


class MeddlingMiddleware(object):
    def process_request(self, request):
        return HttpResponseRedirect('/foobarbaz')


class StaticTemplateTests(SimpleTestCase):
    def setUp(self):
        super(StaticTemplateTests, self).setUp()
        if LooseVersion(django.get_version()) < LooseVersion('1.8'):
            settings.TEMPLATE_LOADERS = ['statictemplate.tests.TestLoader']
        else:
            settings.TEMPLATES[0]['OPTIONS']['loaders'] = ['statictemplate.tests.TestLoader']

    def test_python_api(self):
        output = make_static('simple')
        self.assertEqual(output, 'headsimple')

    def test_call_command(self):
        sio = StringIO()
        call_command('statictemplate', 'simple', stdout=sio)
        self.assertEqual(sio.getvalue().strip(), 'headsimple')

    def test_request_command(self):
        sio = StringIO()
        call_command('statictemplate', 'request', stdout=sio,
                     extra_request='extra=extra_request&canonical=1')
        self.assertEqual(sio.getvalue().strip(), 'headrequest extra_request')

    def test_file_command(self):
        _, sio = mkstemp()
        call_command('statictemplate', 'simple', output=sio)
        with open(sio, 'r') as tmp:
            self.assertEqual(tmp.read().strip(), 'headsimple')

    def test_meddling_middleware(self):
        middleware = (
            'statictemplate.tests.MeddlingMiddleware',
        )
        settings.MIDDLEWARE_CLASSES = middleware
        output = make_static('simple')
        self.assertEqual(output, 'headsimple')
        self.assertEqual(settings.MIDDLEWARE_CLASSES, middleware)

    def test_no_ovveride_middleware(self):
        with self.settings(STATICTEMPLATE_OVERRIDE_MIDDLEWARE=False):
            middleware = (
                'statictemplate.tests.MeddlingMiddleware',
            )
            settings.MIDDLEWARE_CLASSES = middleware
            statictemplate_settings.OVERRIDE_MIDDLEWARE = False
            with self.assertRaises(InvalidResponseError):
                output = make_static('simple')
            statictemplate_settings.OVERRIDE_MIDDLEWARE = True