import json
import time
from typing import Optional

import requests

from authentication.authenticator import IAuthenticator, Token
from authentication.exceptions import AuthInvalidResponseError, AuthConnectionError

REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://play.aidungeon.com"
}
AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={}"
AUTH_REQUEST_JSON = {"returnSecureToken": True}


class AIDAuthenticator(IAuthenticator):
    def __init__(self, authentication_key: str):
        self._authentication_key = authentication_key
        self.token: Optional[Token] = None


    def get_token(self) -> Optional[Token]:
        if self.token and self.token.expired:
            self.token = None
        return self.token


    def login(self) -> None:
        if self.token and not self.token.expired:
            return self.token
        request_time = time.time()
        response = self.send_request()
        token, time_valid = self.parse_response(response)
        self.token = Token(token, request_time+time_valid)
        return self.token

    def send_request(self) -> requests.Response:
        try:
            return requests.post(
                url=AUTH_URL.format(self._authentication_key),
                headers=REQUEST_HEADERS,
                json=AUTH_REQUEST_JSON
            )
        except Exception as ex:
            raise AuthConnectionError(ex) from ex

    @staticmethod
    def parse_response(response: requests.Response) -> tuple:
        try:
            parsed_response = response.json()
            token: str = "firebase " + parsed_response["idToken"]
            time_valid: float = float(parsed_response["expiresIn"])
        except (json.JSONDecodeError, KeyError) as ex:
            raise AuthInvalidResponseError(ex) from ex
        return token, time_valid



