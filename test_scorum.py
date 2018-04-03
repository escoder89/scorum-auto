import time
import random
import logging
import pytest
from datetime import datetime, timedelta

from scorum.constants import StatusCode, BASE_FORMAT
from scorum.utils import (
    get_config,
    get_logger,
    HttpRequest
)
from scorum.models import (
    Request,
    BlockResponse,
    DynamicGlobalPropertiesResponse
)


CONFIG = get_config()
NODES = CONFIG['nodes']
FIRST_BLOCK_TIMESTAMP = CONFIG['first_block_timestamp']
BLOCKS_PRODUCTION_INTERVAL = int(CONFIG['blocks_production_interval'])


class TestScorum:

    @pytest.fixture(scope="class")
    def logger(self) -> logging.Logger:
        return get_logger(level=logging.DEBUG)

    @pytest.fixture(scope="class")
    def client(self, logger):
        return HttpRequest(scheme=get_config()['scheme'], logger=logger)

    @pytest.mark.parametrize('node', NODES)
    def test_get_first_block_info(self, node: str, client: HttpRequest):
        client.host = node
        req = Request(params=["database_api", "get_block", [1]])
        resp = client.send_post_request(payload=req, resp_type=BlockResponse)
        assert resp.result.timestamp == FIRST_BLOCK_TIMESTAMP
        assert not int(resp.result.previous)

    @pytest.mark.parametrize('node', NODES)
    def test_get_next_blocks_info(self, node: str, client: HttpRequest):
        client.host = node
        timestamp = datetime.strptime(FIRST_BLOCK_TIMESTAMP, BASE_FORMAT)
        block_id = None
        for idx in range(2, 12):
            timestamp += timedelta(seconds=BLOCKS_PRODUCTION_INTERVAL)
            req = Request(params=["database_api", "get_block", [idx]])
            resp = client.send_post_request(payload=req, resp_type=BlockResponse)
            assert resp.result.timestamp == timestamp.strftime(BASE_FORMAT)
            if block_id:
                assert resp.result.previous == block_id
            block_id = resp.result.block_id

    @pytest.mark.parametrize('node', NODES)
    def test_check_blocks_generation_with_interval(self, node: str, client: HttpRequest):
        client.host = node
        req = Request(params=["database_api", "get_dynamic_global_properties", []])
        resp = client.send_post_request(payload=req, resp_type=DynamicGlobalPropertiesResponse)
        block_number = resp.result.head_block_number
        while True:
            resp = client.send_post_request(payload=req, resp_type=DynamicGlobalPropertiesResponse)
            if resp.result.head_block_number != block_number:
                block_number = resp.result.head_block_number
                block_time = resp.result.time
                break
        start = time.time()
        for _ in range(5):
            resp = client.send_post_request(payload=req, resp_type=DynamicGlobalPropertiesResponse)
            if (time.time() - start) < BLOCKS_PRODUCTION_INTERVAL:
                assert resp.result.head_block_number == block_number
                assert resp.result.time == block_time
            else:
                block_number += 1
                assert resp.result.head_block_number == block_number
                block_time = datetime.strptime(block_time, BASE_FORMAT) + timedelta(
                    seconds=BLOCKS_PRODUCTION_INTERVAL)
                block_time = block_time.strftime(BASE_FORMAT)
                assert resp.result.time == block_time
                start = time.time()
            time.sleep(1)

    @pytest.mark.parametrize('node', NODES)
    def test_get_block_info_nonexistent_id(self, node: str, client: HttpRequest):
        client.host = node
        for id in [-1, 0, random.randint(10**6, 10**9)]:
            req = Request(params=["database_api", "get_block", [id]])
            resp = client.send_post_request(payload=req, resp_type=BlockResponse)
            assert not resp.id
            assert not resp.result

    @pytest.mark.parametrize('node', NODES)
    def test_get_block_info_no_id(self, node: str, client: HttpRequest):
        client.host = node
        req = Request(params=["database_api", "get_block", []])
        client.send_post_request(payload=req, expected_code=StatusCode.BAD_REQUEST)

    @pytest.mark.parametrize('node', NODES)
    def test_get_block_info_invalid_id(self, node: str, client: HttpRequest):
        client.host = node
        req = Request(params=["database_api", "get_block", ['invalid']])
        client.send_post_request(payload=req, expected_code=StatusCode.BAD_REQUEST)

    @pytest.mark.parametrize('node', NODES)
    def test_get_block_info_invalid_method(self, node: str, client: HttpRequest):
        client.host = node
        req = Request(method="invalid", params=["database_api", "get_block", [1]])
        client.send_post_request(payload=req, expected_code=StatusCode.BAD_REQUEST)

    @pytest.mark.parametrize('node', NODES)
    def test_request_no_params(self, node: str, client: HttpRequest):
        client.host = node
        req = Request(params=[])
        client.send_post_request(payload=req, expected_code=StatusCode.BAD_REQUEST)
