# -*- coding: utf-8 -*-
import requests

import facebook

fb = facebook.FacebookMessenger()


class FineDustRequest:
    def pm_grader(self, response, recipient_id, si_do, gu):
        data = response.json()

        pm10_value = str(data['list'][0]['pm10Value'])
        pm25_value = str(data['list'][0]['pm25Value'])

        pm10_grade = str(data['list'][0]['pm10Grade'])
        pm25_grade = str(data['list'][0]['pm25Grade'])

        if int(pm10_grade) == 1 and int(pm25_grade) == 1:
            pm10_text_grade = '좋음'
            special_message = '맑은 하늘이네요! 안심하시고 나가셔도 됩니다 🥰'
        elif 2 <= int(pm25_grade) * int(pm10_grade) <= 4:
            pm10_text_grade = '보통'
            special_message = '그럭저럭 괜찮네요! 😉'
        elif 5 <= int(pm25_grade) * int(pm10_grade) <= 8:
            pm10_text_grade = '나쁨'
            special_message = '꼭 마스크 챙기시고 나가셔야겠네요! 😷'
        elif 9 <= int(pm25_grade) * int(pm10_grade):
            pm10_text_grade = '매우 나쁨'
            special_message = '오늘은 나가시지 않는게 좋을 것 같네요;;; 😱'
        else:
            pm10_text_grade = 'N/A'
            special_message = '미세먼지 데이터에 문제가 생긴 것 같습니다; 서비스에 불편 드려 죄송합니다 😅'

        if pm25_grade == '1':
            pm25_text_grade = '좋음'
        elif pm25_grade == '2':
            pm25_text_grade = '보통'
        elif pm25_grade == '3':
            pm25_text_grade = '나쁨'
        elif pm25_grade == '4':
            pm25_text_grade = '매우 나쁨'
        else:
            pm25_text_grade = 'N/A'

        if si_do != "" and gu != "":
            custom_text = si_do + " " + gu
        elif si_do != "" and gu == "":
            custom_text = si_do
        elif si_do == "" and gu != "":
            custom_text = gu
        else:
            custom_text = "N/A"
        send_message = "\"" + custom_text + "\": \n\n" + "미세먼지 농도: " + pm10_value \
                       + "μg/㎥ " + "(" + pm10_text_grade + "),\n" + "초미세먼지 농도: " + \
                       pm25_value + "μg/㎥ " + "(" + pm25_text_grade + ") 입니다." + "\n\n" + special_message
        print('>>> 미세먼지 송출 메시지: \n\n' + send_message)
        fb.send_text_message(recipient_id, send_message)

        if response.status_code == 200:
            print('>> 애플리케이션: "미세먼지 API"로부터 StatusCode 200을 받았습니다.')

    # 방식은 Get 방식
    def today_dust_request(self, recipient_id, si_do, gu):
        gu_req_url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/" \
                     "getMsrstnAcctoRltmMesureDnsty?ServiceKey=n9ncCn2UecqURdAD62GyviK7CrTlgyCW" \
                     "z7QapI49OZS3sma05WTl5k1whigvxcA0nwMdHyUpGhwSz2O0qBnseA%3D%3D&stationName=" + gu + \
                     "&dataTerm=DAILY&_returnType=json"
        sido_req_url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/" \
                       "getCtprvnRltmMesureDnsty?ServiceKey=n9ncCn2UecqURdAD62GyviK7CrTlgyCW" \
                       "z7QapI49OZS3sma05WTl5k1whigvxcA0nwMdHyUpGhwSz2O0qBnseA%3D%3D&sidoName=" + si_do + \
                       "&dataTerm=DAILY&_returnType=json"

        # TODO: Send w/ Params. (NOT DIRTY URL)

        if si_do != "" and gu != "":
            response = requests.get(url=gu_req_url)
            self.pm_grader(response, recipient_id, si_do, gu)
        elif si_do != "" and gu == "":
            response = requests.get(url=sido_req_url)
            self.pm_grader(response, recipient_id, si_do, gu)
        elif si_do == "" and gu != "":
            response = requests.get(url=gu_req_url)
            self.pm_grader(response, recipient_id, si_do, gu)
        else:
            fb.send_text_message(recipient_id, '다시 입력해주세요!')

            return {
                "result": "success"
            }
