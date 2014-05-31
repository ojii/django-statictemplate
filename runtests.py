# -*- coding: utf-8 -*-
import sys

urlpatterns = []

TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}


INSTALLED_APPS = [
    'statictemplate',
]

ROOT_URLCONF = 'runtests'


def runtests():
    from django.conf import settings
    settings.configure(
        INSTALLED_APPS=INSTALLED_APPS,
        ROOT_URLCONF=ROOT_URLCONF,
        DATABASES=DATABASES,
        TEST_RUNNER='django.test.simple.DjangoTestSuiteRunner',
        TEMPLATE_DEBUG=TEMPLATE_DEBUG,
        TEMPLATE_CONTEXT_PROCESSORS=[
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.i18n',
            'django.core.context_processors.debug',
            'django.core.context_processors.request',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'django.core.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            ]
    )

    # Run the test suite, including the extra validation tests.
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)

    test_runner = TestRunner(verbosity=1, interactive=False, failfast=False)
    failures = test_runner.run_tests(INSTALLED_APPS)
    return failures


if __name__ == "__main__":
    failures = runtests()
    if failures:  # pragma: no cover
        sys.exit(bool(failures))
