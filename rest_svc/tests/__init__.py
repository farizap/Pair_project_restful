# tests/__init__.py

import pytest, json, logging
from flask import Flask, request

from blueprints import app
from app import cache

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)


def create_token():
    # token = cache.get('test-token')
    token = None

    if token is None:
        ##prepare request input
        data = {
            'client_key':'CLIENT02',
            'client_secret':'SECRET02'
        }
        # do request

        req = call_client(request)
        res = req.get('/token', 
                        query_string=data)

        ## store responese
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        # assert /compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('test-token', res_json['token'], timeout=60)

        ## return, because it useful for other test
        return res_json['token']
    else:
        return token


def create_token_noninternal():
    token = cache.get('test-token-noninternal')

    if token is None:
        ##prepare request input
        data = {
            'client_key':'CLIENT01',
            'client_secret':'SECRET01'
        }
        # do request

        req = call_client(request)
        res = req.get('/token', 
                        query_string=data)

        ## store responese
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        # assert /compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('test-token-noninternal', res_json['token'], timeout=60)

        ## return, because it useful for other test
        return res_json['token']
    else:
        return token