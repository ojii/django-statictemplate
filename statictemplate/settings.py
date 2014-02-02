# -*- coding: utf-8 -*-
from django.conf import settings
STATICTEMPLATE_OVERRIDE_MIDDLEWARE = getattr(settings, 'STATICTEMPLATE_OVERRIDE_MIDDLEWARE', False)