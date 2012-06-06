Bundle
******

Class ``Bundle`` is similar to flasks Blueprint with one important
difference - ``Bundle`` is a class, when blueprints are instances.

Thats all.
Small example how it works::

    from flask.ext.bundle import Bundle, expose

    class News(Bundle):
        
        @expose('/', methods=['GET', 'POST'])
        def index(self):
            return 'Ok'

APIs
****

Based on bundle we have some helpers to build APIs in ``flask.ext.bundle.api``.

bundle.utils
------------

check_data
==========

Decorator for views, get ``Trafaret`` instance. Will return errors dict and status 400
on error.

encode_result
=============

Decorator for result encoding, gets list of encoders. Each encoder must implement two methods,
``mimes`` that returns MIME codes, and ``encode(self, data, mime=None)`` that encode data to response string.


APIBundle
---------

Extensions to ``Bundle`` to make API explorable (TODO write more)
