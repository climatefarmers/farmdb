import json

import pytest

from .parser import parse_survey, split_street, MISSING_STREET_NR


@pytest.fixture()
def survey_response_body():
    with open('./example_body.json', 'r') as f:
        body = json.load(f)
    return body


def test_survey_parser(survey_response_body):
    parsed = parse_survey(survey_response_body)
    assert parsed['person']['email'] == "an_account@example.com"
    assert parsed['person']['comm_pref']['comm_channel'] == 2


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ('Foobar Str. 345', ['345', 'Foobar Str.']),
        ('6 Whatever Lane', ['6', 'Whatever Lane']),
        ('Am alten Rathaus', [MISSING_STREET_NR, 'Am alten Rathaus'])
    ]
)
def test_split_street(test_input, expected):
    out = split_street(test_input)
    assert out == expected