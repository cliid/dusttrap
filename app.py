# -*- coding: utf-8 -*-
"""
DUSTTRAP™ Server v1

Written by JW Jang.
All rights reserved.

for more, please see: https://github.com/HackerJang
"""

import os

from flask import Flask, request, jsonify, redirect, render_template

import key
from facebook import FacebookMessenger
from finedust import FineDustRequest
from nlp import NaturalLanguageProcessing

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dialogflow_key.json'

app = Flask(__name__)

dust_version = 'v1.0a.1000.01.r1'


@app.route('/')
def redirect_v1():
    return redirect('/v1.0/')


@app.route('/support/bugreport', methods=['GET', 'POST'])
def bug_report():
    global_id = 0
    if request.method == 'GET':
        request_id = request.args.get('id')
        if request_id is not None:
            return render_template('support/bugreport/index.html', id=request_id)
        else:
            return render_template('support/error/index.html')
    if request.method == 'POST':
        suggestions = request.form['suggestions']
        bug = request.form['bug']
        print(suggestions + bug)
        return suggestions + bug


@app.route('/v1.0/')
def hello():
    return 'DustTrap™ Server API'


@app.route('/v1.0/webhook', methods=['GET', 'POST'])
def messenger():
    if request.method == 'GET':
        # GET 방식 (Verification)
        from key import VERIFY_TOKEN
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Verification Token이 올바르지 않습니다! 토큰 값을 다시 확인하세요.'

    if request.method == 'POST':
        # POST 방식 (Actual Request from FB)
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
                            nlp = NaturalLanguageProcessing()

                            project_id = key.DIALOGFLOW_PROJECT_ID
                            intent = nlp.return_intent(project_id, key.SESSION_ID, request_str, key.DLC)

                            # Intent: 인사하기
                            if intent == '인사':
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    fb.qr_know_me(recipient_id)
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        fb.qr_know_me(recipient_id)
                                    else:
                                        message = user_info['error']
                                        fb.send_text_message(recipient_id, message)
                                continue

                            # Intent: 미세먼지 데이터 가져오기
                            elif intent == '미세먼지':
                                gu = nlp.return_gu(request_str, key.DLC)
                                si_do = nlp.return_sido(request_str, key.DLC)
                                try:
                                    dt.today_dust_request(recipient_id, si_do, gu)
                                    fb.qr_fine_dust(recipient_id, si_do, gu)
                                except:
                                    fb.qr_default(recipient_id, '죄송하지만 요청하신 곳의 미세먼지 데이터가 없습니다.\n'
                                                                '시/군/구의 이름으로 다시 시도해주시면 감사하겠습니다. :)')
                                continue

                            elif intent == '버그':
                                fb.qr_default(recipient_id, '아래 버튼을 눌러서 신고해주세요!')
                                fb.send_bug(recipient_id)
                                continue

                            elif intent == '웃김':
                                fb.qr_default(recipient_id, 'ㅋㅋㅋㅋ')
                                continue

                            elif intent == '이상함':
                                fb.qr_default(recipient_id, '헤엣?')
                                continue

                            elif intent == '더보기':
                                fb.qr_know_more(recipient_id)
                                fb.send_more(recipient_id)
                                continue

                            elif intent == '소스코드':
                                fb.qr_default(recipient_id, '미세봇™ 의 소스코드입니다.')
                                fb.send_source_code(recipient_id)
                                continue
                            else:
                                fb.send_text_message(recipient_id, '넹?')
                                fb.send_text_message(recipient_id, '무슨 뜻인지 잘 모르겠어요.')
                                continue

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
                                # <시작하기> 경우

                                # 사용자 정보 가져오기
                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)
                                username = user_info['data']['last_name'] + user_info['data']['first_name']

                                if user_info['result'] == 'success':
                                    fb.send_text_message(recipient_id, '안녕하세요, ' + username + ' 님!')
                                    fb.qr_start(recipient_id)
                                    continue
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        fb.qr_start(recipient_id)
                                        continue
                                    else:
                                        message = user_info['error']
                                        fb.send_text_message(recipient_id, message)
                                        continue

                            elif payload == "BUG_REPORT":
                                # <버그 신고하기> 경우

                                # 사용자 정보 가져오기
                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    fb.send_bug(recipient_id)
                                    continue
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        fb.send_bug(recipient_id)
                                        continue
                                    else:
                                        message = user_info['error']
                                        fb.send_text_message(recipient_id, message)
                                        continue

                            elif payload == "KNOW_ME":
                                # <그래!> 경우

                                # 사용자 정보 가져오기
                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    fb.qr_know_me(recipient_id)
                                    continue
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        fb.qr_know_me(recipient_id)
                                        continue
                                    else:
                                        message = user_info['error']
                                        fb.qr_default(recipient_id)
                                        fb.send_text_message(recipient_id, message)
                                        continue

                            elif payload == "KNOW_MORE":
                                # <더 알아볼래!> 경우

                                # 사용자 정보 가져오기
                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    fb.qr_know_more(recipient_id)
                                    fb.send_message(recipient_id, '미세봇™ 은 '
                                                                  '실시간 미세먼지 + α 페메봇입니다! 🧐')
                                    fb.send_more(recipient_id)
                                    continue
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        fb.qr_know_more(recipient_id)
                                        fb.send_message(recipient_id, '미세봇™ 은 '
                                                                      '미세먼지 실시간 확인 페메봇입니다! 🧐')
                                        fb.send_more(recipient_id)
                                        continue
                                    else:
                                        message = user_info['error']
                                        fb.qr_default(recipient_id)
                                        fb.send_text_message(recipient_id, message)
                                        continue

                            elif payload == "HOW_TO_USE":
                                # <쓰는 법 알아보기> 경우

                                # 사용자 정보 가져오기
                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    fb.qr_default(recipient_id)
                                    fb.send_message(recipient_id, '이렇게 해보세요:')
                                    fb.send_message(recipient_id, '> 내일 강남구 미세먼지\n'
                                                                  '> 어제 강남구 미세먼지 좀 알려줘!\n'
                                                                  '> 강남구')
                                    fb.send_message(recipient_id, 'AI의 힘 덕분에 원하시는 대로 말할 수도 있어요. 한번 마음대로 불러 주세요✌')
                                    continue
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        fb.qr_default(recipient_id)
                                        fb.send_message(recipient_id, '이렇게 해보세요:')
                                        fb.send_message(recipient_id, '> 내일 강남구 미세먼지\n'
                                                                      '> 어제 강남구 미세먼지 좀 알려줘!\n'
                                                                      '> 강남구')
                                        fb.send_message(recipient_id, 'AI의 힘 덕분에 원하시는 대로 말할 수도 있어요. 한번 마음대로 불러 주세요✌')
                                        continue
                                    else:
                                        message = user_info['error']
                                        fb.qr_default(recipient_id)
                                        fb.send_text_message(recipient_id, message)
                                        continue

                            elif payload == "IN_DEVELOPMENT":
                                # <아직 개발중> 경우

                                # 사용자 정보 가져오기
                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    fb.qr_default(recipient_id)
                                    fb.send_message(recipient_id, '아직 개발중입니다! 🥳')
                                    continue
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        fb.qr_default(recipient_id)
                                        fb.send_message(recipient_id, '아직 개발중입니다! 🥳')
                                        continue
                                    else:
                                        message = user_info['error']
                                        fb.qr_default(recipient_id)
                                        fb.send_text_message(recipient_id, message)
                                        continue

                            elif payload == "LOOK_SOURCE":
                                # <소스코드 볼래!> 경우

                                # 사용자 정보 가져오기
                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    fb.qr_default(recipient_id, '미세봇™ 의 소스코드입니다.')
                                    fb.send_source_code(recipient_id)
                                    continue
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        fb.qr_default(recipient_id, '미세봇™ 의 소스코드입니다.')
                                        fb.send_source_code(recipient_id)
                                        continue
                                    else:
                                        message = user_info['error']
                                        fb.qr_default(recipient_id, '미세봇™ 의 소스코드입니다.')
                                        fb.send_text_message(recipient_id, message)
                                        continue

                            elif payload == "USAGE_TIP":
                                # <팁 보기> 경우

                                # 사용자 정보 가져오기
                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    fb.send_source_code(recipient_id)
                                    fb.qr_default(recipient_id)
                                    continue
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        fb.send_source_code(recipient_id)
                                        fb.qr_default(recipient_id)
                                        continue
                                    else:
                                        message = user_info['error']
                                        fb.qr_default(recipient_id)
                                        fb.send_text_message(recipient_id, message)
                                        continue

                            else:
                                # <위를 제외한 모든 경우>

                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    fb.qr_default(recipient_id)
                                    continue
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        fb.qr_default(recipient_id)
                                        continue
                                    else:
                                        message = user_info['error']
                                        fb.qr_default(recipient_id)
                                        fb.send_text_message(recipient_id, message)
                                        continue
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
