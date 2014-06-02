#####################
Django Statictemplate
#####################

.. image:: https://pypip.in/version/django-statictemplate/badge.png
    :target: https://pypi.python.org/pypi/django-statictemplate/
    :alt: Latest Version

.. image:: https://travis-ci.org/yakky/django-statictemplate.svg
    :target: https://travis-ci.org/yakky/django-statictemplate
    :alt: Travis status

.. image:: https://coveralls.io/repos/yakky/django-statictemplate/badge.png
    :target: https://coveralls.io/r/yakky/django-statictemplate
    :alt: Coveralls status

.. image:: https://pypip.in/download/django-statictemplate/badge.png
    :target: https://pypi.python.org/pypi//django-statictemplate/
    :alt: Download

.. image:: https://pypip.in/wheel/django-statictemplate/badge.png
    :target: https://pypi.python.org/pypi/django-statictemplate/
    :alt: Wheel Status

.. image:: https://pypip.in/license/django-statictemplate/badge.png
    :target: https://pypi.python.org/pypi/django-statictemplate/
    :alt: License


This project aims at providing a compromise between dynamic error pages for
Django (that use template tags etc and therefore potentially error too) and
having to write static error pages by hand.

It does so by providing a management command that can be invoked to turn a
dynamic Django template into a static HTML page with no template tags
whatsoever in it.

Note that this means that every time you change your error pages, you need to
re-run this script. Ideally this is part of your deploy process.


************
Installation
************

``pip install django-statictemplate`` inside your virtualenv.

Add ``statictemplate`` to your ``INSTALLED_APPS``.


*************
Configuration
*************

``django-statictemplate`` does not require any configuration. by default.


By default ``django-statictemplate`` overrides the configured middlewares for
enhanced compatibility and to avoid incompatibilities.

However this may not be always feasible: if you need a specific set of
middlewares to be loaded set::

    STATICTEMPLATE_OVERRIDE_MIDDLEWARE = False

in you settings files.

Please note that ``django-statictemplate`` has not been tested with every
possible middleware, thus you may encounter failures and strange behaviors
especially fi you use middlewares that changes the response type.


*****
Usage
*****

``python manage.py statictemplate dynamic_500.html > 500.html``

or

``python manage.py statictemplate dynamic_500.html -f 500.html``

The management command renders a template given by name (standard Django
template name resolution applies) and writes the output to stdout or to a file.

=========
Arguments
=========

* ``template``: standard django template name to render
* ``language``: sets the client django_language cookie to render page in the
  given language
* ``extra_request``: extra parameters injected in the request. Parameters must
  be serialized in querystring format (e.g.: ``'variable=value&variable=value'``;
  please note the single quote **'** to protect ampersand **&**).

=======
Options
=======

* ``-f``, ``--file``: file destionation for command output

*******
License
*******

This project is licensed under the BSD license.


************
Contributors
************

See https://github.com/ojii/django-statictemplate/contributors
