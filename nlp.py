import json

import dialogflow_v2 as df
import requests

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

    def return_gu(self, text, language_code):
        request_url = self.DIALOGFLOW_URL + key.SESSION_ID + ":detectIntent"
        headers = {'Content-Type': 'application/json', 'charset': 'utf-8',
                   'Authorization': 'Bearer ya29.c.Kl61B2iIUvf0kHCpwwfAcTY25FvnbZSB9QW_'
                                    '9AyRzhaERUqPzLJ3Dx_koAwel6qQ4i9UtbRZRRh6Im15GObGVf'
                                    'yNe1bAafWUv_snlqc0uHGevm3qPwSCswEt56EbKTFy'}
        parameters = {
            "queryInput": {
                "text": {
                    "text": text,
                    "languageCode": language_code
                }
            },
            "queryParams": {
                "timeZone": "Asia/Seoul"
            }
        }
        print('>>>>> NLP return_gu() function working now...')
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)
        sel_gu = response.json()['queryResult']['parameters']['selected_gu']

        return sel_gu
