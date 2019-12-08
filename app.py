"""
DUSTTRAP™ Server v1

Written by JW Jang.
All rights reserved.

for more, please see: https://github.com/HackerJang
"""

from flask import Flask, request, jsonify, redirect, make_response
import dialogflow

from facebook import FacebookMessenger
from google.api_core.exceptions import InvalidArgument
import key

app = Flask(__name__)

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
                            session_client = dialogflow.SessionsClient()
                            session = session_client.session_path(key.DIALOGFLOW_PROJECT_ID, key.SESSION_ID)
                            text_input = dialogflow.types.TextInput(text=request_str, language_code=key.DIALOGFLOW_LANGUAGE_CODE)
                            query_input = dialogflow.types.QueryInput(text=text_input)

                            try:
                                response = session_client.detect_intent(session=session, query_input=query_input)
                                intent = response.query_result.intent.display_name
                            except InvalidArgument:
                                raise Exception('Something Strange Happened')

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
                                # TODO: 미세먼지 API 이용해서 잘 파싱하고 쿼리해서 거기서 Response 받고 잘 처리하기.
                                user_info = fb.get_user_info(recipient_id)

                                fb.send_text_message('아직 미구현입니다!')

                            else:
                                message = '구현되지 않은 인텐트입니다.'
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
                                # <시작하기> 경우

                                # <--- 베타 안내 메시지 시작

                                # 사용자 정보 가져오기
                                fb = FacebookMessenger()
                                user_info = fb.get_user_info(recipient_id)

                                if user_info['result'] == 'success':
                                    message = '안녕하세요, %s%s 님, 처음 만나서 반가워요! 저는 미세봇™ 입니다.' \
                                              '베타라서 일부 기능이 제대로 작동하지 않을 수 있어요.\n' \
                                              '만약 버그를 발견했을 때에는, 저를 만든 분(https://m.me/hackerjang) 에게 ' \
                                              '페메로 스크린샷과 함께 제보해 주시면 정말 감사하겠습니다.\n좋은 하루 보내세요!' \
                                              '' % (user_info['data']['last_name'], user_info['data']['first_name'])
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
    app.run(host='0.0.0.0', port=8082)
