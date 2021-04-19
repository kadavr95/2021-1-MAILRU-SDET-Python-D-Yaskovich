import logging
from urllib.parse import urljoin

import requests
from requests.cookies import cookiejar_from_dict


logger = logging.getLogger('test')

MAX_RESPONSE_LENGTH = 500


class ResponseErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class InvalidLoginException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

        self.csrf_token = None
        self.sessionid_gtp = None

    @staticmethod
    def log_pre(method, url, headers, data, expected_status):
        logger.info(f'Performing {method} request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
                    f'expected status: {expected_status}\n\n')

    @staticmethod
    def log_post(response):
        log_str = 'Got response:\n' \
                  'RESPONSE STATUS: {response.status_code}'

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
                            f'Use DEBUG logging.\n\n')
            elif logger.level == logging.DEBUG:
                logger.debug(f'{log_str}\n'
                             f'RESPONSE CONTENT: {response.text}\n\n')
        else:
            logger.info(f'{log_str}\n'
                        f'RESPONSE CONTENT: {response.text}\n\n')

    def _request(self, method, location, headers=None, data=None, expected_status=200, jsonify=True):
        url = urljoin(self.base_url, location)

        self.log_pre(method, url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data)
        self.log_post(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')

        if jsonify:
            json_response = response.json()
            if json_response.get('bStateError'):
                error = json_response.get('bErrorMsg', 'Unknown')
                raise ResponseErrorException(f'Request "{url}" return error "{error}"!')
            return json_response
        return response

    @property
    def post_headers(self):
        return {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    def get_token(self):
        headers = self._request('GET', self.base_url, jsonify=False).headers['Set-Cookie'].split(';')
        token_header = [h for h in headers if 'csrftoken' in h]
        if not token_header:
            raise Exception('CSRF token not found in main page headers')

        token_header = token_header[0]
        token = token_header.split('=')[-1]

        return token

    def post_login(self, user, password):
        location = 'https://auth-ac.my.com/auth?lang=ru&nosavelogin=0'

        # csrf_token = self.get_token()

        headers = self.post_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Connection'] = 'keep-alive'
        headers['Origin'] = 'https://target.my.com'
        headers['Referer'] = 'https://target.my.com/'
        headers['Host'] = 'auth-ac.my.com'
        headers['Upgrade-Insecure-Requests'] = '1'

        data = {
            'login': user,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }

        result = self._request('POST', location, headers=headers, data=data, jsonify=False)
        try:
            response_cookies = result.headers['Set-Cookie'].split(';')
        except Exception as e:
            raise InvalidLoginException(e)

        new_csrf_token = [c for c in response_cookies if 'csrftoken' in c][0].split('=')[-1]
        sessionid_gtp = [c for c in response_cookies if 'sessionid_gtp' in c][0].split('=')[-1]

        self.session.cookies = cookiejar_from_dict({'csrftoken': new_csrf_token, 'sessionid_gtp': sessionid_gtp})
        self.csrf_token = new_csrf_token
        self.sessionid_gtp = sessionid_gtp

        return result