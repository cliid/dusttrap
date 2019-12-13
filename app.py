"""
DUSTTRAP™ Server v1

Written by JW Jang.
All rights reserved.

for more, please see: https://github.com/HackerJang
"""

import os

from flask import Flask, request, jsonify, redirect

import key
import nlp
from facebook import FacebookMessenger
from finedust import FineDustRequest

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dialogflow_key.json'

app = Flask(__name__, static_url_path='')

mw_version = 'v1.0a.1000.01.r1'


@app.route('/')
def redirect_v1():
    return redirect('/v1.0/')


@app.route('/v1.0/')
def hello():
    return 'What the 버-억'


@app.route('/v1.0/webhook', methods=['GET', 'POST'])
def messenger():
    if request.method == 'GET':
        # GET 방식으로 접속한 경우, Verification Test 중이다.
        from key import VERIFY_TOKEN
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Verification Token이 올바르지 않습니다! 토큰 값을 다시 확인하세요.'

    if request.method == 'POST':
        try:
            req = request.get_json()
            print('>> 디버그: Webhook 요청 JSON:\n%s' % str(req))

            for event in req['entry']:
                # 메시지
                for e in event['messaging']:
                    if e.get('message'):
                        recipient_id = e['sender']['id']

                        # 텍스트 메시지일 때
                        if e['message'].get('text'):
                            request_str = e['message'].get('text')

                            # <--- '진짜' 메시지 시작

                            # 객체 선언
                            fb = FacebookMessenger()
                            dt = FineDustRequest()

                            project_id = key.DIALOGFLOW_PROJECT_ID
                            intent = nlp.return_intent(project_id, key.SESSION_ID, request_str, key.DLC)

                            # Intent: 인사하기
                            if intent == '인사':
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    message = '안녕하세요, %s%s 님! 👋' \
                                              '' % (user_info['data']['last_name'], user_info['data']['first_name'])
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        message = '안녕하세요! 👋'
                                    else:
                                        message = user_info['error']

                            # Intent: 미세먼지 데이터 가져오기
                            elif intent == '미세먼지':
                                message = '송파구의 미세먼지는 다음과 같습니다.'
                                dt.today_dust_request(recipient_id, "송파구")

                            elif intent == '버그':
                                fb.send_text_message(recipient_id, '아래 버튼을 눌러서 신고해주세요!')
                                fb.send_bug(recipient_id)
                                continue

                            elif intent == '웃김':
                                message = 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ'

                            elif intent == '이상함':
                                message = '헤엣?'

                            else:
                                message = '넹?'
                                fb.send_text_message(recipient_id, message)
                                message = '무슨 뜻인지 잘 모르겠어요.'
                                fb.send_text_message(recipient_id, message)
                                continue

                            fb.send_text_message(recipient_id, message)

                        # 첨부파일이 있는 메시지일 때
                        if e['message'].get('attachments'):
                            for att in e['message'].get('attachments'):
                                fb = FacebookMessenger()
                                fb.send_message(recipient_id, ':)')

                    # Postback 처리하기
                    elif e.get('postback'):
                        recipient_id = e['sender']['id']

                        if e['postback'].get('payload'):
                            payload = e['postback']['payload']

                            # Payload 값에 따라 분기
                            if payload == "FACEBOOK_WELCOME":
                                # <시작하기> or <Get Started> 경우

                                # <--- 인사/안내 시작

                                # 사용자 정보 가져오기
                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    fb.send_quick_reply_start(recipient_id)
                                    # TODO: 도움말
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        message = '안녕하세요, 처음 만나서 반가워요! 저는 미세봇™ 입니다.' \
                                                  '베타라서 일부 기능이 제대로 작동하지 않을 수 있어요.\n' \
                                                  '만약 버그를 발견했을 때에는, 저를 만든 분(https://m.me/hackerjang) 에게 ' \
                                                  '페메로 스크린샷과 함께 제보해 주시면 정말 감사하겠습니다.\n좋은 하루 보내세요!'

                                    else:
                                        message = user_info['error']
                                        fb.send_text_message(recipient_id, message)
                                        continue

                                fb.send_text_message(recipient_id, message)
                                continue

                                # 베타 안내 메시지 끝! --->
                        else:
                            pass
            return {
                "result": "success"
            }
        except Exception as e:
            # 치명적이다, 원혁.

            print('>> 오류!!! UNKNOWN - 처리되지 않은 예외 - %s' % str(e))

            return {
                "result": "error"
            }


class InvalidUsage(Exception):
    # 오류를 처리하기 위한 클래스: InvalidUsage(message, status_code=None, payload=None) 로 사용하세요.
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    # 에러 핸들러.
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
