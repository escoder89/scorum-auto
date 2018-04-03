import json
import urllib3
import requests
import logging

from typing import Type, Union

from scorum.constants import StatusCode, Headers
from scorum.models import (
    StatusCodeError,
    BlockResponse,
    DynamicGlobalPropertiesResponse
)


def get_config() -> dict:
    with open("config.json") as f:
        return json.load(f)


def get_logger(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(level)
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    return logger


def assert_status_code(actual: requests.Response, expected: int):
    if actual.status_code != expected:
        raise StatusCodeError("Status code: {} != {},\nResponse:{}".
                              format(actual.status_code, expected, actual.text))


class HttpRequest:

    urllib3.disable_warnings()

    def __init__(self, scheme: str, logger: logging.Logger, host: str = None):
        self.host = host
        self.scheme = scheme
        self.logger = logger

    @property
    def base_url(self) -> str:
        return "{}://{}".format(self.scheme, self.host)

    def send_post_request(self, path: str = None,
                          headers: dict = Headers.ContentTypeText,
                          payload: object = None,
                          resp_type: Type = None,
                          expected_code: int = None) -> Union[BlockResponse,
                                                              DynamicGlobalPropertiesResponse]:
        if path:
            url = "{}/{}".format(self.base_url, path)
        else:
            url = self.base_url
        self.logger.debug("Request body:\n{}".format(payload.__dict__))
        resp = requests.post(url, headers=headers, json=payload.__dict__, verify=False)
        if expected_code:
            assert_status_code(resp, expected_code)
        else:
            assert_status_code(resp, StatusCode.OK)
        resp = resp.json()
        self.logger.debug("Response body:\n{}".format(resp))
        if resp_type:
            return resp_type(**resp)
        else:
            return resp
