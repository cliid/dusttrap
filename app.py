"""
DUSTTRAP™ Server v1

Written by JW Jang.
All rights reserved.

for more, please see: https://github.com/HackerJang
"""

from flask import Flask, request, jsonify, redirect
import datetime
import pytz

from facebook import FacebookMessenger
from nlp import NaturalLanguageProcessing as NativeNLP, LuisAI

app = Flask(__name__)

mw_version = 'v1.0a.1000.01.r1'


@app.route('/')
def redirect_v1():
    return redirect('/v1.0/')


@app.route('/v1.0/')
def hello():
    return {
        "result": "success",
        "message": "Fuck You."
    }


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
                            luis = LuisAI()

                            # NativeNLP 처리
                            try:
                                nlp_result = luis.think(request_str)
                                intent = nlp_result['topScoringIntent']['intent']
                            except KeyError:
                                # 이럴 일은 없어야만 한다.

                                print('>> 에러!: LUIS.ai Quota 초과!')
                                fb.send_text_message(recipient_id, "에러!: MW_NLP_QUOTA")

                                continue

                            # print('>> 디버그: \'%s\' 에 대한 NativeNLP 처리 결과:\n%s' % (request_str, nlp_result))

                            # Intent: 인사하기
                            if intent == '인사':
                                user_info = fb.get_user_info(recipient_id)  # 사용자 정보 가져오기

                                if user_info['result'] == 'success':
                                    message = '안녕하세요, %s%s 님! 👋' \
                                              '' % (user_info['data']['last_name'], user_info['data']['first_name'])
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        message = '안녕하세요! 👋'
                                    else:
                                        message = user_info['error']

                            # Intent: 급식 가져오기
                            elif intent == '미세':
                                # TODO: ASYNC

                                # 미완성 경고 메시지
                                message = '저는 아직 미완성이랍니다.'
                                fb.send_text_message(recipient_id, message)

                                entities = [[], []]
                                for item in nlp_result['entities']:
                                    entities[0].append(item['type'])
                                    entities[1].append(item['entity'].strip())

                                if 'SchoolName' in entities[0]:
                                    # TODO: 안 더럽게
                                    school_name = entities[1][entities[0].index('SchoolName')]
                                        continue

                                    # 안내 메시지 발송
                                    # print('>> 디버그: %s -> %s 학교의 급식을 가져옵니다...'
                                    #       '' % (recipient_id, school_name))
                                    # fb.send_text_message(recipient_id, school_name + '의 급식을 가져옵니다!')

                                    # 학교 조회
                                    sc = School()
                                    school_info = sc.get_school_info(school_name)

                                    if len(school_info) == 0:  # 학교가 없음
                                        fb.send_text_message(
                                            recipient_id,
                                            '학교 \'%s\'를 찾을 수 없어요.' % school_name
                                        )
                                        continue

                                    elif len(school_info) > 1:  # 학교가 여러 개임
                                        # TODO: 구현

                                        message = '검색된 지역이 여러 개여서 미세먼지 데이터를 가져올 수 없어요.\n' \
                                                  '정확한 이름으로 다시 시도해주세요.\n' \
                                                  '(완벽하게 이름이 같은 경우에는 추후에 우선적으로 구현 예정입니다):\n'
                                        for school in school_info:
                                            message = message + ' ' + school['school_name']

                                        fb.send_text_message(recipient_id, message)
                                        continue

                                    else:  # 1개 학교가 정상적으로 조회된 경우
                                        nl = NativeNLP()

                                        if 'DynamicDate' in entities[0]:
                                            d_date_string = entities[1][entities[0].index('DynamicDate')]
                                            date = nl.string_to_date(d_date_string)
                                        else:
                                            date = datetime.datetime.now(pytz.timezone('Asia/Seoul')).date()

                                        meal = sc.get_meal(school_info[0], date=date)

                                        if len(meal) < 1:
                                            message = "%d년 %d월 %d일 %s에는 급식이 없어요! 😉\n" \
                                                      "(또는 나이스에 등록이 안된 것일수도 있어요✅)" \
                                                      % (int(date.year),
                                                         int(date.month),
                                                         int(date.day),
                                                         school_info[0]['school_name'])
                                        else:
                                            message = '%d년 %d월 %d일 %s의 급식이에요! 😀\n' \
                                                      % (int(date.year),
                                                         int(date.month),
                                                         int(date.day),
                                                         school_info[0]['school_name'])
                                            for food in meal:
                                                message = message + '\n' + food

                                        fb.send_text_message(recipient_id, message)
                                        continue

                                else:  # 학교 이름이 요청 메시지에 없는 경우
                                    message = '학교 이름을 포함해서 다시 요청해 주세요.'
                                    fb.send_text_message(recipient_id, message)
                                    continue

                            else:
                                message = '구현되지 않은 인텐트입니다: ' + nlp_result['topScoringIntent']['intent']
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
                                    message = '안녕하세요, %s%s 님, 처음 만나서 반가워요! 저는 급식봇™ 베타입니다.' \
                                              '베타라서 일부 기능이 제대로 작동하지 않을 수 있어요.\n' \
                                              '만약 버그를 발견했을 때에는, 저를 만든 분(https://m.me/computerpark05) 에게 ' \
                                              '페메로 스크린샷과 함께 제보해 주시면 정말 감사하겠습니다.\n좋은 하루 보내세요!' \
                                              '' % (user_info['data']['last_name'], user_info['data']['first_name'])
                                    # TODO: 도움말
                                else:
                                    if user_info['code'] == 'FB_PAGE':
                                        message = '안녕하세요, 처음 만나서 반가워요! 저는 급식봇™ 베타입니다.' \
                                                  '베타라서 일부 기능이 제대로 작동하지 않을 수 있어요.\n' \
                                                  '만약 버그를 발견했을 때에는, 저를 만든 분(https://m.me/computerpark05) 에게 ' \
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
