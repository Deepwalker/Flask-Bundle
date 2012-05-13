from werkzeug import routing
from flask import url_for


def expose(url='/', **kwargs):
    def view(f):
        if not hasattr(f, '_urls'):
            f._urls = []
        f._urls.append((url, kwargs))
        return f
    return view


class Bundle(routing.Submount):

    def __init__(self, name, path):
        self.name = name
        self.endpoints = {}
        self.leaf = None # Special workaround to be able add (path + '') url

        self.path = path
        self.rules = list(self._get_rules())
        super(Bundle, self).__init__(path, self.rules)

    def _get_rules(self):
        for name in dir(self):
            view = getattr(self, name)
            if not hasattr(view, '_urls'):
                continue
            endpoint = self.endpoint_name(name)
            self.endpoints[endpoint] = view
            for url, kwargs in view._urls:
                if url == '':
                    self.leaf = routing.Rule(
                             self.path, endpoint = endpoint, **kwargs)
                    continue
                yield routing.Rule(url, endpoint = endpoint, **kwargs)

    def endpoint_name(self, name):
        return '%s.%s' % (self.name, name)

    def url_for(self, name, **kwargs):
        return url_for(self.endpoint_name(name), **kwargs)

    def push_bundle(self, app):
        self.app = app
        app.url_map.add(self)
        if self.leaf:
            app.url_map.add(self.leaf)
        for endpoint, view in self.endpoints.iteritems():
            app.endpoint(endpoint)(self.wrapper(view))

    def wrapper(self, view):
        "Use it to decorate all bundle views"
        return view
