import requests

import facebook
import key

fb = facebook.FacebookMessenger()


# 방식은 Get 방식
class FineDustRequest:
    JusoReqURL = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"

    def today_dust_request(self, recipient_id, station_name):
        URL = self.JusoReqURL + "?ServiceKey=" + key.OPENAPI_SERVICE_KEY + "&stationName=" \
              + station_name + "&dataTerm=DAILY&_returnType=json"
        response = requests.get(URL)
        fb.send_text_message(recipient_id, response)
