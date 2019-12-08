import requests
import datetime
import pytz


class LuisAI:
    NLP_SUBSCRIPTION_KEY = '5d71a9e3c2bf469f880a914ca78db078'
    NLP_APP_ID = 'bcd6bad8-1b8c-4d57-9b9e-a5c2adb03d9b'
    NLP_URL = 'https://mealworm3.cognitiveservices.azure.com/luis/v2.0luis/prediction/v3.0/apps/' + NLP_APP_ID + '/slots/production/predict'

    def think(self, talk):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.NLP_SUBSCRIPTION_KEY,
        }

        params = {
            # Query parameter
            'q': talk,
            # Optional request parameters, set to default values
            'timezoneOffset': '540',    # 60 x 9 -> UTC+9 (Asia/Seoul)
            'verbose': 'false',
            'spellCheck': 'false',
            'staging': 'false',
        }

        r = requests.get(
            self.NLP_URL,
            headers=headers, params=params)
        return r.json()


class NaturalLanguageProcessing:
    @staticmethod
    def string_to_date(string):
        string = string.strip().replace(' ', '')

        if string == '내일':
            return (datetime.datetime.now(pytz.timezone('Asia/Seoul')) + datetime.timedelta(days=1)).date()
        elif string == '오늘':
            return datetime.datetime.now(pytz.timezone('Asia/Seoul')).date()
        elif string == '어제':
            return (datetime.datetime.now(pytz.timezone('Asia/Seoul')) + datetime.timedelta(days=-1)).date()

        return datetime.datetime.now(pytz.timezone('Asia/Seoul')).date()
