import logging

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

question_index = {
    'lBUQO8sOX12x' : 'full_name',
    'gu1WRpwodKDM' : 'email',
    'rdSMIPaen13X' : 'phone',
    'FUbrknB8bw1r' : 'farm_name',
    'uzugPvjVFU2F' : 'farm_website',
    'BxLQkXrnalNC' : 'street',
    '3Bh3mTnRojgi' : 'city',
    'TH0TmwYqIOlW' : 'country',
    'XTQrsUU9IvoK' : 'comm_pref',
    '7AIAa8JbmMzd' : 'farm_description',
    'DsEKgxgmmbXi' : 'production_methods',
    'dxFiOS8gg3pq' : 'main_products',
    'xTTq3HponTHi' : 'farm_size_approx',
    'VdUp9RxHGy6t' : 'soil',
    'ugKrLtCARW2r' : 'tillage',
    'v1RIdlGEDiOT' : 'fertilization',
    'jaTU4yiTzorr' : 'irrigation',
    'GC0ocjfxDxXa' : 'uses_icides',
    '0Eno9oaL2iTf' : 'receives_funding',
}



def parse_survey(survey_body: dict) -> dict:
    """Parses survey responses as sent by the TypeForm webhook.

    Args:
        survey_body (dict): The survey body a sent by TypeForm webhook

    Returns:
        dict: Parsed answers
    """
    fields = {f.pop('id'): f for f in survey_body['form_response']['definition']['fields']}
    answers = survey_body['form_response']['answers']
    parsed  = {}
    for answer in answers:
        field_id = answer['field']['id']
        answer_type = answer['type']
        field_prompt = fields[field_id]['title']

        try: 
            field_name = question_index[field_id]
        except KeyError as e:
            logger.warning(f"Question ID {field_id} with prompt '{field_prompt}' not in question index.")
            continue

        if answer_type == 'choices':
            answer_content = answer[answer_type]['labels']
        elif answer_type == 'choice':
            answer_content = answer[answer_type]['label']
        else:
            answer_content = answer[answer_type]

        if field_name == 'full_name':
            name_parts = answer_content.split(' ')
            first_name, last_name = ' '.join(name_parts[:-1]), name_parts[-1]
            parsed['first_name'] = first_name
            parsed['last_name'] = last_name
        else:
            parsed[field_name] = answer_content

    return parsed