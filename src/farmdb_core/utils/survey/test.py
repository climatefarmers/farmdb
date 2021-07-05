import json

import pytest

from .parser import parse_survey


@pytest.fixture()
def survey_response_body():
    with open('./example_body.json', 'r') as f:
        body = json.load(f)
    return body


def test_survey_parser(survey_response_body):
    parsed = parse_survey(survey_response_body)
    assert parsed['person']['email'] == "an_account@example.com"
    assert parsed['person']['comm_pref']['comm_channel'] == 2