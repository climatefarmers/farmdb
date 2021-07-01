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
    assert parsed['email'] == "an_account@example.com"
    assert parsed['comm_pref'] == ["Barcelona"]