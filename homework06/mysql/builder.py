from mysql.models import TotalRequests, RequestOfType, FrequentRequest, BigFailedRequest, ThreatOrigin


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_total_requests(self, requests_count=None, filename=None):
        if requests_count is None:
            requests_count = 0

        total_requests = TotalRequests(
            requests_count=requests_count,
            filename=filename
        )
        self.client.session.add(total_requests)
        self.client.session.commit()  # no need if sessionmaker autocommit=True
        return total_requests

    def create_request_of_type(self, requests_type=None, requests_count=None, filename=None):
        if requests_type is None:
            requests_type = "UNKNOWN"

        if requests_count is None:
            requests_count = 0

        request_of_type = RequestOfType(
            requests_type=requests_type,
            requests_count=requests_count,
            filename=filename
        )
        self.client.session.add(request_of_type)
        self.client.session.commit()  # no need if sessionmaker autocommit=True
        return request_of_type

    def create_frequent_request(self, url=None, requests_count=None, filename=None):
        if url is None:
            url = '/'

        if requests_count is None:
            requests_count = 0

        frequent_request = FrequentRequest(
            url=url,
            requests_count=requests_count,
            filename=filename
        )
        self.client.session.add(frequent_request)
        self.client.session.commit()  # no need if sessionmaker autocommit=True
        return frequent_request

    def create_big_failed_request(self, url=None, error_code=None, size=None, origin_ip=None, filename=None):
        if url is None:
            url = '/'

        if error_code is None:
            error_code = 418

        if size is None:
            size = 0

        if origin_ip is None:
            origin_ip = '127.0.0.1'

        big_failed_request = BigFailedRequest(
            url=url,
            error_code=error_code,
            size=size,
            origin_ip=origin_ip,
            filename=filename
        )
        self.client.session.add(big_failed_request)
        self.client.session.commit()  # no need if sessionmaker autocommit=True
        return big_failed_request

    def create_threat_origin(self, origin_ip=None, requests_count=None, filename=None):
        if origin_ip is None:
            origin_ip = '127.0.0.1'

        if requests_count is None:
            requests_count = 0

        threat_origin = ThreatOrigin(
            origin_ip=origin_ip,
            requests_count=requests_count,
            filename=filename
        )
        self.client.session.add(threat_origin)
        self.client.session.commit()  # no need if sessionmaker autocommit=True
        return threat_origin
