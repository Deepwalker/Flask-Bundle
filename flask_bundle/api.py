from werkzeug import routing
from . import Bundle

"""
API Bundle is bundle that generate some JSON
description about endpoints.
"""

class APIBundle(Bundle):

    def push_bundle(self, app):
        super(APIBundle, self).push_bundle(app)
        if not hasattr(app, 'api_set'):
            app.api_set = []
        app.api_set.append(self)

    def browse_api(self):
        for name, view in self.endpoints.items():
            for url in view._urls:
                u = url[0]
                methods = url[1].get('methods', ['GET'])
                host, converted_url, args = convert_url(self.path + u)
                yield {'name': name, 'host': host, 'url': converted_url,
                       'methods': methods, 'args': args, 'desc': view.__doc__,
                       'path': name.split('.')}


class MethodCaller(object):

    def __init__(self, method, host=None):
        self.method = method
        self.host = host

    def gen_url(self, **kwargs):
        host = self.method['host'] or self.host
        return 'http://%s/%s' % (host, self.method['url'].format(**kwargs))

    def __call__(self, **kwargs):
        import urllib2
        url = self.gen_url(**kwargs)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(url)
        data = opener.open(request)
        return data.read()


class APICaller(object):

    def __init__(self, host, caller=MethodCaller):
        self.map_ = routing.Map()
        self.host = host
        self.caller = caller

    def get_leaf(self, path):
        leaf = self
        for node in path:
            if not hasattr(leaf, node):
                setattr(leaf, node, APICaller(self.host, self.caller))
            leaf = getattr(leaf, node)
        return leaf

    def add_method(self, method_name, host, url, methods, args, desc):
        setattr(self, method_name, self.caller({'name': method_name,
                'url': url, 'methods': methods, 'desc': desc,
                'host': host, 'args': args}, host=self.host))


def dump_api(app):
    for api in app.api_set:
        for method in api.browse_api():
            yield method


def generate_api(api_dump, host, caller=MethodCaller):
    root = APICaller(host, caller)
    for method in api_dump:
        api_path = method['name'].split('.')
        root.get_leaf(api_path[:-1]).add_method(
                api_path[-1], method['host'], method['url'], method['methods'],
                method['args'], method['desc'])
    return root


def convert_url(werkzeug_url):
    m = routing.Map()
    r = routing.Rule(werkzeug_url)
    r.bind(m)
    url = ''.join('{%s}' % node if is_arg else node
                  for is_arg, node in r._trace)
    host, url = url.split('|', 1)
    return host, url, list(r.arguments)
