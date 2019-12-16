import json

import dialogflow_v2 as df
import requests
from google_oauth import ServiceAccount

import key


class NaturalLanguageProcessing:
    DIALOGFLOW_URL = "https://dialogflow.googleapis.com/v2/projects/dusttrap-qoacwk/agent/sessions/"

    def return_intent(self, project_id, session_id, text, language_code):
        session_client = df.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        if text:
            text_input = df.types.TextInput(text=text, language_code=language_code)
            query_input = df.types.QueryInput(text=text_input)
            response = session_client.detect_intent(session=session, query_input=query_input)
            return response.query_result.intent.display_name

    def return_gu(self, project_id, session_id, text, language_code):
        oauth_key = json.load(open('dialogflow_key.json'))
        scope = 'https://www.googleapis.com/auth/dialogflow'
        auth = ServiceAccount.from_json(key=oauth_key, scopes=scope)
        request_url = self.DIALOGFLOW_URL + key.SESSION_ID + ":detectIntent"
        headers = {'Content-Type': 'application/json', 'charset': 'utf-8', 'Authorization': 'Bearer ' +
                                                                                            auth.access_token}
        parameters = {
            "queryInput": {
                "text": {
                    "text": text,
                    "languageCode": language_code
                }
            }
        }
        print('>>>>> NLP return_gu() function working now...')
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)
        sel_gu = response.json()['queryResult']['parameters']['selected_gu']

        return sel_gu

    def return_sido(self, project_id, session_id, text, language_code):
        oauth_key = json.load(open('dialogflow_key.json'))
        scope = 'https://www.googleapis.com/auth/dialogflow'
        auth = ServiceAccount.from_json(key=oauth_key, scopes=scope)
        request_url = self.DIALOGFLOW_URL + key.SESSION_ID + ":detectIntent"
        headers = {'Content-Type': 'application/json', 'charset': 'utf-8', 'Authorization': 'Bearer ' +
                                                                                            auth.access_token}
        parameters = {
            "queryInput": {
                "text": {
                    "text": text,
                    "languageCode": language_code
                }
            }
        }
        print('>>>>> NLP return_sido() function working now...')
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)
        sel_sido = response.json()['queryResult']['parameters']['selected_sido']

        return sel_sido
