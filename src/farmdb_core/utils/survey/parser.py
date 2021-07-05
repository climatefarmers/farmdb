import logging
import re

logger = logging.getLogger(__name__)

""" Example json data:

field = {
            "id":"gu1WRpwodKDM",
            "title":"Email Address",
            "type":"email",
            "ref":"3fc030ef-859d-4dd4-af70-bd3a6ec00a77",
            "properties":{}
        }

answer = {
            "type":"email",
            "email":"an_account@example.com",
            "field":{
               "id":"gu1WRpwodKDM",
               "type":"email",
               "ref":"3fc030ef-859d-4dd4-af70-bd3a6ec00a77"
            }
         }

choice_answer = {
            "type":"choice",
            "choice":{
               "label":"Barcelona"
            },
            "field":{
               "id":"TH0TmwYqIOlW",
               "type":"multiple_choice",
               "ref":"e4142f74-e5cf-43b7-a3f8-d83486d4bc23"
            }
         }

choices_answer {
            "type":"choices",
            "choices":{
               "labels":[
                  "Barcelona"
               ]
            },
            "field":{
               "id":"XTQrsUU9IvoK",
               "type":"multiple_choice",
               "ref":"b6ce5e15-48da-4bd1-ac1a-30150aefaf98"
            }
         },

"""

FARMER_ROLE_ID = 1
MISSING_STREET_NR = -99

question_index = {
    'lBUQO8sOX12x': 'full_name',  # -> first_name, last_name
    'gu1WRpwodKDM': 'email',
    'rdSMIPaen13X': 'phone',
    'FUbrknB8bw1r': 'farm_name',
    'uzugPvjVFU2F': 'farm_website',
    'BxLQkXrnalNC': 'street',
    '3Bh3mTnRojgi': 'city',
    'TH0TmwYqIOlW': 'country',
    'XTQrsUU9IvoK': 'comm_pref',
    '7AIAa8JbmMzd': 'farm_type',
    'DsEKgxgmmbXi': 'production_methods',
    'dxFiOS8gg3pq': 'main_products',
    'xTTq3HponTHi': 'farm_size_approx',
    'VdUp9RxHGy6t': 'soil',
    'ugKrLtCARW2r': 'tillage',
    'v1RIdlGEDiOT': 'fertilization',
    'jaTU4yiTzorr': 'irrigation',
    'GC0ocjfxDxXa': 'uses_icides',
    '0Eno9oaL2iTf': 'receives_funding',
}


def determine_answer_content(answer):
    answer_type = answer['type']
    if answer_type == 'choices':
        return answer[answer_type]['labels']
    elif answer_type == 'choice':
        return answer[answer_type]['label']
    return answer[answer_type]


def split_name(full_name):
    name_parts = full_name.split(' ')
    return ' '.join(name_parts[:-1]), name_parts[-1]


def split_street(street):
    splits = re.split(r'(?<=\d)(?:-\d+)?\s+', street)
    if len(splits) == 1:
        return MISSING_STREET_NR, splits[0]
    return splits


def lookup_comm_pref(comm_pref):
    options = {
        "Phone Call" : 1,
        "Email" : 2,
        "WhatsApp" : 3
    }
    return options.get(comm_pref[0], 2) # default to email


def flatten_survey(survey_body: dict) -> dict:
    """Parses survey responses as sent by the TypeForm webhook.

    Args:
        survey_body (dict): The survey body a sent by TypeForm webhook

    Returns:
        dict: flattened answers
    """
    fields = {
        f.pop('id'): f for f in survey_body['form_response']['definition']['fields']}
    answers = survey_body['form_response']['answers']
    flattened = {}
    for answer in answers:
        field_id = answer['field']['id']

        field_prompt = fields[field_id]['title']

        try:
            field_name = question_index[field_id]
        except KeyError as e:
            logger.warning(
                f"Question ID {field_id} with prompt '{field_prompt}' not in question index.")
            continue

        answer_content = determine_answer_content(answer)

        if field_name == 'full_name':
            flattened['first_name'], flattened['last_name'] = split_name(answer_content)
        elif field_name == 'street':
            flattened['street_number'], flattened['route'] = split_street(answer_content)
        elif field_name == 'comm_pref':
            flattened[field_name] = lookup_comm_pref(answer_content)
        elif field_name == 'farm_size_approx':
            flattened[field_name] = int(answer_content) if answer_content.isdigit() else None
        else:
            flattened[field_name] = answer_content

    return flattened


def parse_address(**kwargs):
    return {
        'street_number': kwargs.get('street_number'),
        'route': kwargs.get('route', ''),
        'raw': ' '.join([str(e) for e in [
            kwargs.get('route', ''),
            kwargs.get('street_number', ''),
            kwargs.get('city', ''),
            kwargs.get('country', ''),
        ]]),
        'locality': {
            'name': kwargs.get('city', ''),
            'state': {
                'name': kwargs.get('state', ''),
                'country': {
                    'name': kwargs.get('country', ''),
                },
            },
        }
    }


def parse_person(**kwargs):
    return {
        'first_name': kwargs.get('first_name'),
        'last_name': kwargs.get('last_name'),
        'email': kwargs.get('email'),
        'phone': kwargs.get('phone'),
        'address': kwargs.get('address'),
        'comm_pref': {
            'comm_channel': kwargs.get('comm_pref'),
        }
    }


def parse_survey_answers(**kwargs):
    return {
        'farm_type': kwargs.get('farm_type'),
        'production_methods': kwargs.get('production_methods'),
        'main_products': kwargs.get('main_products'),
        'soil': kwargs.get('soil'),
        'tillage': kwargs.get('tillage'),
        'fertilization': kwargs.get('fertilization'),
        'irrigation': kwargs.get('irrigation'),
        'uses_icides': kwargs.get('uses_icides'),
        'receives_funding': kwargs.get('receives_funding'),
        }


def parse_farm(**kwargs):
    return {
        'name': kwargs.get('farm_name'),
        'website': kwargs.get('farm_website'),
        'address': kwargs.get('address'),
        'farm_size_approx': kwargs.get('farm_size_approx'),
        'survey_answers': kwargs.get('survey_answers'),
    }

def parse_survey(survey_body: dict) -> dict:
    flattened = flatten_survey(survey_body)

    address = parse_address(**flattened)
    person = parse_person(**flattened, address=address)
    survey_answers = parse_survey_answers(**flattened)
    farm = parse_farm(**flattened, address=address, survey_answers=survey_answers)    
    return {
        'person': person,
        'organization':farm,
        'role':{
            'role' : FARMER_ROLE_ID
        }
    }