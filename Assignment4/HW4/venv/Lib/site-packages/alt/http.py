from alt.common import get_default_logger
import requests
from urllib.parse import urljoin


def invoke_rest_method(**kwargs):
        """
        Invokes a rest api test
        :param kwargs:
            REQUIRED:

            method = 'GET', 'POST', 'PUT', 'DELETE'

            url = "http://localhost/api/controller"
                or
            baseurl = "http://localhost/"
            endpoint = "api/controller"

            OPTIONAL:

            headers = {'header_name':'header_value', 'header2_name':'header2_value'}

            json = {'key1':'value1', 'key2':'value2'}   #Will be sent as json encoded data
                or
            form = {'key1':'value1', 'key2':'value2'}   #Will be sent as form encoded data

            api_key = "ey123asdk93e378hsdfsfdf"
            silent = True,False  (to not log request/response. Default False)
        :return:
        """
        logger = kwargs.get('logger', get_default_logger())
        args = {}
        headers = kwargs.get('headers', {})
        api_key = kwargs.get('api_key', None)
        if api_key is not None:
            headers['Authorization'] = api_key
        if headers is not {}:
            args['headers'] = headers
        json = kwargs.get('json', None)
        if json is not None:
            args['json'] = json
        form = kwargs.get('form', None)
        if form is not None:
            args['data'] = form
        if json is not None and form is not None:
            raise ValueError('Cannot specify both json and form parameters')
        url = kwargs.get('url', None)
        if url is None:
            baseurl = kwargs.get('baseurl', None)
            endpoint = kwargs.get('endpoint', None)
            if baseurl is None or endpoint is None:
                raise ValueError('Invalid test arguments. Must specify {url} or {baseurl, endpoint}')
            url = urljoin(baseurl, endpoint)
        method = kwargs.get('method', None)
        if method is None:
            raise ValueError('Invalid test arguments. Must specify {method}')
        silent = kwargs.get('silent', False)
        if not silent:
            logger.debug("Sending {} to url: {}".format(method, url))
        req = requests.request(method, url, **args)
        if not silent:
            logger.debug("Received response code: {}".format(req.status_code))
        return req