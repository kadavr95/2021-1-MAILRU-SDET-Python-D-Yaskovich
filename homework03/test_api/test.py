import pytest

from api.client import InvalidLoginException
from test_api.base import ApiBase


class TestApi(ApiBase):

    def test_valid_login(self, credentials):
        self.api_client.post_login(*credentials)

    def test_invalid_login(self):
        with pytest.raises(InvalidLoginException):
            self.api_client.post_login('123', '456')
            pytest.fail('Login unexpectedly succeeded')
