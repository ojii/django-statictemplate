#####################
Django Statictemplate
#####################

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


*****
Usage
*****

``python manage.py statictemplate dynamic_500.html > 500.html``

The management command renders a template given by name (standard Django
template name resolution applies) and writes the output to stdout, so you
should redirect stdout to a filename.

=========
Arguments
=========

 * ``template``: standard django template name to render
 * ``language``: sets the client django_language cookie to render page in the
   given language
 * ``extra_request``: extra parameters injected in the request. Parameters must
   be serialized in querystring format (e.g.: ``'variable=value&variable=value'``;
   please note the single quote **'** to protect ampersand **&**).


*******
License
*******

This project is licensed under the BSD license.


************
Contributors
************

See https://github.com/ojii/django-statictemplate/contributors
