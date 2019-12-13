import requests

import facebook

fb = facebook.FacebookMessenger()


# 방식은 Get 방식
class FineDustRequest:
    JusoReqURL = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/" \
                 "getMsrstnAcctoRltmMesureDnsty?ServiceKey=n9ncCn2UecqURdAD62GyviK7CrTlgyCW" \
                 "z7QapI49OZS3sma05WTl5k1whigvxcA0nwMdHyUpGhwSz2O0qBnseA%3D%3D&stationName=송파구" \
                 "&dataTerm=DAILY&_returnType=json"

    def today_dust_request(self, recipient_id, station_name):
        # TODO: Send w/ Params. (NOT DIRTY CODE)
        response = requests.get(url=self.JusoReqURL)
        data = response.json()
        pm10_value = str(data['list'][0]['pm10Value'])

        fb.send_text_message(recipient_id, "미세먼지 농도는 " + pm10_value + "μg/m^3 입니다.")

        if response.status_code == 200:
            print('>> 애플리케이션: 미세먼지 API로부터 StatusCode 200을 받았습니다.')

            return {
                "result": "success"
            }
