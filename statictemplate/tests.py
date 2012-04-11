# -*- coding: utf-8 -*-
from StringIO import StringIO
from django.conf import settings
from django.core.management import call_command
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from statictemplate.management.commands.statictemplate import make_static
import unittest


class TestLoader(BaseLoader):
    is_usable = True
    templates = {
        'simple': '{% extends "base" %}{% block content %}simple{% endblock %}',
        'base': '{% block head %}head{% endblock %}{% block content %}content{% endblock %}',
    }
    def load_template_source(self, template_name, template_dirs=None):
        found = self.templates.get(template_name, None)
        if not found: # pragma: no cover
            raise TemplateDoesNotExist(template_name)
        return found, template_name


class StaticTemplateTests(unittest.TestCase):
    def setUp(self):
        settings.TEMPLATE_LOADERS = ['statictemplate.tests.TestLoader']
        
    def test_python_api(self):
        output = make_static('simple')
        self.assertEqual(output, 'headsimple')
    
    def test_call_command(self):
        sio = StringIO()
        call_command('statictemplate', 'simple', stdout=sio)
        self.assertEqual(sio.getvalue(), 'headsimple')
    