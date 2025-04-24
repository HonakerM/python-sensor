import logging
from typing import Generator
import pytest

from instana.util.config import parse_ignored_endpoints_from_yaml


class TestConfigReader:
    @pytest.fixture(autouse=True)
    def _resource(self) -> Generator[None, None, None]:
        yield

    def test_load_file(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.DEBUG, logger="instana")

        ignore_endpoints = parse_ignored_endpoints_from_yaml(
            "tests/util/test_configuration-1.yaml"
        )
        # test with tracing
        assert ignore_endpoints == [
            "redis.get",
            "redis.type",
            "dynamodb.query",
            "kafka.consume.span-topic",
            "kafka.consume.topic1",
            "kafka.consume.topic2",
            "kafka.send.span-topic",
            "kafka.send.topic1",
            "kafka.send.topic2",
            "kafka.consume.topic3",
            "kafka.*.span-topic",
            "kafka.*.topic4",
        ]

        ignore_endpoints = parse_ignored_endpoints_from_yaml(
            "tests/util/test_configuration-2.yaml"
        )
        assert ignore_endpoints == [
            "redis.get",
            "redis.type",
            "dynamodb.query",
            "kafka.consume.span-topic",
            "kafka.consume.topic1",
            "kafka.consume.topic2",
            "kafka.send.span-topic",
            "kafka.send.topic1",
            "kafka.send.topic2",
            "kafka.consume.topic3",
            "kafka.*.span-topic",
            "kafka.*.topic4",
        ]
        assert (
            'Please use "tracing" instead of "com.instana.tracing"' in caplog.messages
        )
