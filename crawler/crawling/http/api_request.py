import json
from urllib.parse import urljoin
import logging

import requests

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class APIRequest(object):
    """
    This base request can be instantiated with a base URL for an API.
    Subsequent calls can be made with the usual arguments for :meth:`requests.request`, specifying only the API route::
        >>> api_request = APIRequest('http://example.com/api/v3')
        >>> response = api_request('POST', '/login', data={'username': 'foo', 'password': 'bar'})
    etc.
    """

    def __init__(self, base_url, headers=None):
        if not base_url.endswith('/'):
            base_url += '/'
        self._base_url = base_url

        if headers is not None:
            self._headers = headers
        else:
            self._headers = {}

    def __call__(self, method, route, **kwargs):

        # Account for flask-like routes
        if route.startswith('/'):
            route = route[1:]

        url = urljoin(self._base_url, route, allow_fragments=False)

        headers = kwargs.pop('headers', {})
        headers.update(self._headers)

        response = requests.request(method=method, url=url, headers=headers, **kwargs)

        if 'data' in kwargs:
            log.info(u'{} {} with headers:\n{}\nand data:\n{}'.format(
                method,
                url,
                json.dumps(headers, indent=4),
                json.dumps(kwargs['data'], indent=4)
            ))
        elif 'json' in kwargs:
            log.info(u'{} {} with headers:\n{}\nand JSON:\n{}'.format(
                method,
                url,
                json.dumps(headers, indent=4),
                json.dumps(kwargs['json'], indent=4)
            ))
        else:
            log.info(u'{} {} with headers:\n{}'.format(
                method,
                url,
                json.dumps(headers, indent=4)
            ))

        log.info(
            u'Response to {} {} => {} {}\n{}'.format(
                method,
                url,
                response.status_code,
                response.reason,
                response.text[:100])
        )

        return response

