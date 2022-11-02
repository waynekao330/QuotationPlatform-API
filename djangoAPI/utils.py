import logging

import requests
import ujson as ujson
from django.http import HttpRequest
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
from rest_framework.parsers import JSONParser

from djangoAPI import settings

urlList = getattr(settings, "API_PATH", {})
jwt_login_account = getattr(settings, "JWT_LOGIN_ACCOUNT", {})
# Get an instance of a logger
logger = logging.getLogger(__name__)


def getJsonFromRequest(request: HttpRequest) -> dict:
    return JSONParser().parse(request)


def postAPI(data: dict, url: str) -> dict:
    res = requests.post(url, json=data)
    if res.status_code == 200:
        return res.json()
    else:
        logger.error("code: {}, content: {}".format(res.status_code, res.content))
        print("code: {}, content: {}".format(res.status_code, res.content))
        return None


def patchAPI_with_bearer(data: list, url: str):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    # headers["Authorization"] = "Bearer {}".format(token)
    headers["Content-Type"] = "application/json"
    res = requests.patch(url, json=data, headers=headers, verify=False)
    return res


def get_jwt_token() -> str:
    res = requests.get(urlList.get("JWTLogin"), auth=HTTPBasicAuth(jwt_login_account.get("username")
                                                                   , jwt_login_account.get("password")), verify=False)
    return res.json().get("access_token")


def get_api_without_wait(url: str):
    try:
        requests.get(url, timeout=0.0000000001)
    except requests.exceptions.ReadTimeout:
        pass
