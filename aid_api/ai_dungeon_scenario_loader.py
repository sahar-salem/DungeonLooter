import requests

from aid_api.constants import QUERY
from authentication.authenticator import IAuthenticator
import logging

class AIDungeonAPI:
    '''
    API Used to obtain scenario
    '''

    def __init__(self, authenticator: IAuthenticator):
        self.authenticator: IAuthenticator = authenticator

    def import_scenario(self, short_id: str) -> str:
        """
        Start a session with AI Dungeon and request a scenario from its database API.
        :param short_id: The id of the scenario taken from its URL.
        :return: A string containing the raw AI Dungeon JSON representation of the scenario.
        """
        session_token = self.authenticator.login().token
        variables = {'shortId': short_id, "viewPublished": True}
        response = requests.post("https://api.aidungeon.com/graphql",
                                 headers={"Authorization": session_token},
                                 json={'query': QUERY, 'variables': variables})
        return response.text


