import pytest
import re
from collections import defaultdict
from operator import itemgetter

from mysql.builder import MySQLBuilder
from mysql.models import TotalRequests, RequestOfType, FrequentRequest, BigFailedRequest, ThreatOrigin

FILENAME = "../access.log"
TOTAL_REQUESTS = 225133
REQUESTS_OF_TYPE = {
    "GET": 122095,
    "POST": 102503,
    "PUT": 6,
    "HEAD": 528,
    "g369g=%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIi"
    "wiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2bfCIpOztlY2hvKC"
    "JlNTBiNWYyYjRmNjc1NGFmMDljYzg0NWI4YjU4ZTA3NiIpOztlY2hvKCJ8PC0iKTs7ZGllKCk7GET": 1
}
FREQUENT_REQUESTS = {
    "/administrator/index.php": 103932,
    "/apache-log/access.log": 26336,
    "/": 6940,
    "/templates/_system/css/general.css": 4980,
    "/robots.txt": 3199,
    "http://almhuette-raith.at/administrator/index.php": 2356,
    "/favicon.ico": 2201,
    "/wp-login.php": 1644,
    "/administrator/": 1563,
    "/templates/jp_hotel/css/template.css": 1287
}
BIG_FAILED_REQUESTS = {
    '/index.php?option=com_phocagallery&view=category&id=4025&Itemid=53':
        {
            'URL': '/index.php?option=com_phocagallery&view=category&id=4025&Itemid=53',
            'STATUS_CODE': 404,
            'SIZE': 1417,
            'ORIGIN_IP': '189.217.45.73'
        },
    '/index.php?option=com_phocagallery&view=category&id=7806&Itemid=53': {
        'URL': '/index.php?option=com_phocagallery&view=category&id=7806&Itemid=53',
        'STATUS_CODE': 404,
        'SIZE': 1417,
        'ORIGIN_IP': '189.217.45.73'
    },
    '/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%289168%3D4696%29%20THEN%209168'
    '%20ELSE%209168%2A%28SELECT%209168%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END%29%29&Itemid=53': {
        'URL': '/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%289168%3D4696%29'
               '%20THEN%209168%20ELSE%209168%2A%28SELECT%209168%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END'
               '%29%29&Itemid=53',
        'STATUS_CODE': 404,
        'SIZE': 1417,
        'ORIGIN_IP': '189.217.45.73'
    },
    '/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%281753%3D1753%29%20THEN%201753'
    '%20ELSE%201753%2A%28SELECT%201753%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END%29%29&Itemid=53': {
        'URL': '/index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%281753%3D1753%29'
               '%20THEN%201753%20ELSE%201753%2A%28SELECT%201753%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END'
               '%29%29&Itemid=53',
        'STATUS_CODE': 404,
        'SIZE': 1417,
        'ORIGIN_IP': '189.217.45.73'
    },
    '/index.php?option=com_easyblog&view=dashboard&layout=write': {
        'URL': '/index.php?option=com_easyblog&view=dashboard&layout=write',
        'STATUS_CODE': 404,
        'SIZE': 1397,
        'ORIGIN_IP': '104.129.9.248'
    }
}
THREAT_ORIGINS = {
    "189.217.45.73": 225,
    "82.193.127.15": 4,
    "91.210.145.36": 3,
    "194.87.237.6": 2,
    "198.38.94.207": 2
}


def file_length(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


class MySQLBase:
    prep_results = []

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)

        self.prep_results = self.prepare()


class TestMysql(MySQLBase):

    def prepare(self, filename=FILENAME):
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
        pattern = re.compile(r'(.*?) [\s\S]*?\"([\w\W]*?) ([\w\W]*?) ([\w\W]*?)\" ([\d]*?) ([\w\W]*?) ([\s\S]*)')
        requests_types = []
        urls = []
        sizes = []
        urls_with_meta = []
        origin_ips = []
        for line in lines:
            match = pattern.match(line)
            requests_types += [match.group(2)]
            urls += [match.group(3)]
            if match.group(5)[0] == '4':
                try:
                    current_size = int(match.group(6))
                except ValueError:
                    current_size = 0
                urls_with_meta += [{"url": match.group(3), "status_code": match.group(5), "size": current_size,
                                    "origin_ip": match.group(1)}]
            if match.group(5)[0] == '5':
                origin_ips += [match.group(1)]
            try:
                sizes += [int(match.group(6))]
            except ValueError:
                sizes += [0]
        return {"lines": lines, "requests_types": requests_types, "urls": urls, "sizes": sizes,
                "urls_with_meta": urls_with_meta, "origin_ips": origin_ips}

    def test_total_requests(self, filename=FILENAME):
        self.mysql_builder.create_total_requests(requests_count=file_length(filename), filename=filename)
        assert self.mysql.session.query(TotalRequests).filter_by(filename=filename).first().requests_count == \
               TOTAL_REQUESTS

    def test_requests_of_type(self, filename=FILENAME):
        requests_types = self.prep_results["requests_types"]
        unique_requests_types = list(set(requests_types))
        for unique_requests_type in unique_requests_types:
            self.mysql_builder.create_request_of_type(requests_type=unique_requests_type,
                                                      requests_count=requests_types.count(unique_requests_type),
                                                      filename=filename)
            assert self.mysql.session.query(RequestOfType).filter_by(requests_type=unique_requests_type,
                                                                     filename=filename).first().requests_count == \
                   REQUESTS_OF_TYPE[unique_requests_type]

    def test_frequent_requests(self, filename=FILENAME):
        urls_dict = defaultdict(int)
        for url in self.prep_results["urls"]:
            urls_dict[url] += 1
        counter = 10
        for url in sorted(urls_dict, key=urls_dict.get, reverse=True):
            if counter > 0:
                self.mysql_builder.create_frequent_request(url=url, requests_count=urls_dict[url], filename=filename)
                assert self.mysql.session.query(FrequentRequest).filter_by(url=url,
                                                                           filename=filename).first().requests_count == \
                       FREQUENT_REQUESTS[url]
            counter -= 1

    def test_big_failed_requests(self, filename=FILENAME):
        counter = 5
        for url in sorted(self.prep_results["urls_with_meta"], key=itemgetter('size'), reverse=True):
            if counter > 0:
                self.mysql_builder.create_big_failed_request(url=url['url'], error_code=url['status_code'],
                                                             size=url['size'], origin_ip=url['origin_ip'],
                                                             filename=filename)
                assert (self.mysql.session.query(BigFailedRequest).filter_by(url=url['url'],
                                                                             filename=filename).first().error_code ==
                        BIG_FAILED_REQUESTS[url['url']]['STATUS_CODE'] and
                        self.mysql.session.query(BigFailedRequest).filter_by(url=url['url'],
                                                                             filename=filename).first().size ==
                        BIG_FAILED_REQUESTS[url['url']]['SIZE'] and
                        self.mysql.session.query(BigFailedRequest).filter_by(url=url['url'],
                                                                             filename=filename).first().origin_ip ==
                        BIG_FAILED_REQUESTS[url['url']]['ORIGIN_IP'])
            counter -= 1

    def test_threat_origins(self, filename=FILENAME):
        origin_ips_dict = defaultdict(int)
        for origin_ip in self.prep_results["origin_ips"]:
            origin_ips_dict[origin_ip] += 1
        counter = 5
        for origin_ip in sorted(origin_ips_dict, key=origin_ips_dict.get, reverse=True):
            if counter > 0:
                self.mysql_builder.create_threat_origin(origin_ip=origin_ip, requests_count=origin_ips_dict[origin_ip],
                                                        filename=filename)
                assert self.mysql.session.query(ThreatOrigin).filter_by(origin_ip=origin_ip,
                                                                        filename=filename).first().requests_count == \
                       THREAT_ORIGINS[origin_ip]
            counter -= 1
