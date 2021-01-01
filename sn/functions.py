import requests as r
import asyncio
import json
import clearbit
from sn import config
from django.http import HttpResponse


def get_dict_request(request):
    body_request = request.body.decode('utf-8').split('&')
    title_body_dict = {}
    for el in body_request:
        title, value = el.split('=')
        title_body_dict[title.replace('+', ' ').replace('%40', '@')] = value.replace('+', ' ').replace('%40', '@')
    return title_body_dict


async def get_hunter_verification(body_dict):
    try:
        hunter_io_verifier = r.get('https://api.hunter.io/v2/email-verifier?email={}&api_key={}'
                                   .format(body_dict['email'], config.HUNTER_IO_API_KEY))
        assert hunter_io_verifier.status_code == 200
        hunter_io_verifier_json = hunter_io_verifier.json()
        assert hunter_io_verifier_json['data']['status'] in config.VALID_HUNTER_STATUSES
        return hunter_io_verifier_json
    except AssertionError:
        return HttpResponse(json.dumps({'data': {'error': 'Either mail, or some request data is wrong'}}))


async def get_clearbit_info_account(body_dict):
    clearbit.key = config.CLEARBIT_API_KEY
    clearbit_json = json.dumps({})
    clearbit_request = clearbit.Enrichment.find(email=body_dict['email'], company=body_dict['company'])
    if clearbit_request is not None:
        clearbit_json = json.dumps(clearbit_request)
    return clearbit_json


async def process_api_request(title_body_dict):
    request_hunter_verification = asyncio.create_task(get_hunter_verification(title_body_dict))
    request_clearbit_io = asyncio.create_task(get_clearbit_info_account(title_body_dict))
    await request_hunter_verification
    await request_clearbit_io
    return request_hunter_verification.result(), request_clearbit_io.result()
