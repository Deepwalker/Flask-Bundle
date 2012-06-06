from functools import wraps
import json
from werkzeug.wrappers import Response
from flask import request
import trafaret as t


def check_data(trafaret):
    """ Check request with trafaret Visitor instance """

    def check_data_(method):
        @wraps(method)
        def method_with_check(self, *a, **kw):
            try:
                data = trafaret.check(request)
                kw.update(data)
                return method(self, *a, **kw)
            except t.DataError as error:
                return error.as_dict(), 400
        return method_with_check
    return check_data_


def encode_result(encoders):
    """ Check Accept header for mime against encoders list.
        If not Accept header, encode with first encoder.
    """
    def get_encoder(encoders):
        if not request.accept_mimetypes:
            encoder = encoders[0]
            return encoder, encoder.mimes()[0]

        for encoder in encoders:
            for mime in encoder.mimes():
                if mime in request.accept_mimetypes:
                    return encoder, mime
        return None, repr([mime for mime in encoder.mimes() for encoder in encoders])

    def wrapper(view):
        @wraps(view)
        def inner(*a, **kw):
            encoder, mime = get_encoder(encoders)
            if encoder is None:
                return Response(mime, 406)
            res = view(*a, **kw)
            if isinstance(res, tuple):
                res = (encoder.encode(res[0], mime=mime),) + res[1:]
            else:
                res = (encoder.encode(res, mime=mime), )
            return Response(*res, content_type=mime)
        return inner
    return wrapper


class JSONEncoder(object):
    """ Sample JSON encoder for ``encode_result`` decorator """

    def mimes(self):
        "Return list of mime types supported by encoder"
        return ('application/json', )

    def encode(self, data, mime=None):
        "Encode given data"
        return json.dumps(data)
