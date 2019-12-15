# -*- coding: utf-8 -*-
import json

import requests
import uuid

from key import ACCESS_TOKEN


class FacebookMessenger:
    GRAPH_URL = 'https://graph.facebook.com/v5.0/me/messages?access_token='

    def send_text_message(self, recipient_id, string):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": string
            }
        }

        print('>> 애플리케이션: %s 에게 메시지를 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 메시지를 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

        else:
            if response.json()['error']['code'] == 100:
                print('>> 애플리케이션: %s 는 없는 유저입니다.' % recipient_id)

                # TODO: 블랙리스트

                return {
                    "result": "success"
                }

            else:
                print('>> 에러! 애플리케이션 -> facebook.py -> send_text_message : FB_SEND_UNKNOWN_ERROR')
                print('>> 디버그: 에러 정보: %s' % str(response.content))

                return {
                    "result": "error",
                    "error": "메시지를 보낼 수 없어요. 메시지를 보내는 도중 에러가 발생했어요. - FB_SEND_UNKNOWN_ERROR",
                    "code": "FB_SEND_UNKNOWN_ERROR"
                }

    def send_message(self, recipient_id, string):
        # Is an alias of send_text_message()
        return self.send_text_message(recipient_id, string)

    def send_bug(self, recipient_id):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "버그 신고하기",
                                "image_url": "https://dust.api.mlsp.kr/images/BugReport.png",
                                "subtitle": "아래 버튼을 클릭하면 버그 신고 양식으로 연결됩니다. 감사합니다.",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "https://dust.api.mlsp.kr/support/bugreport?id=" + str(uuid.uuid4()),
                                        "title": "신고하러 가기"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        print('>> 애플리케이션: %s 에게 템플릿을 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 템플릿을 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

    def send_more(self, recipient_id):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "미세먼지 불러오기",
                                "image_url": "https://dust.api.mlsp.kr/images/FineDust.png",
                                "subtitle": "전국의 미세먼지 데이터를 눈 깜빡할 사이에 불러올 수 있어요.",
                                "buttons": [
                                    {
                                        "type": "postback",
                                        "title": "쓰는 법 알아보기",
                                        "payload": "HOW_TO_USE"
                                    }
                                ]
                            },
                            {
                                "title": "가상의 여자친구",
                                "image_url": "https://dust.api.mlsp.kr/images/UMP45.png",
                                "subtitle": "여친이 없는 당신을 위한 가상의 여자친구.",
                                "buttons": [
                                    {
                                        "type": "postback",
                                        "title": "아직 개발중",
                                        "payload": "IN_DEVELOPMENT"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        print('>> 애플리케이션: %s 에게 템플릿을 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 템플릿을 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

    def send_source_code(self, recipient_id):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "소스 코드",
                                "image_url": "https://dust.api.mlsp.kr/images/Github.png",
                                "subtitle": "현재는 보안 문제로 소스코드가 비공개화 된 점 양해 부탁드립니다.\n"
                                            "소스코드가 보고 싶으신 분들은 \n"
                                            "'anonymous.whoru.human@gmail.com'\n"
                                            "으로 연락 주시면 최대한 빠르게 답변 드리도록 하겠습니다!",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "https://github.com/HackerJang",
                                        "title": "DustTrap™ API Source"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        print('>> 애플리케이션: %s 에게 소스코드 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 소스코드를 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

    def send_who_made_it(self, recipient_id):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "누가 만들었어?",
                                "image_url": "https://dust.api.mlsp.kr/images/Github.png",
                                "subtitle": "미세봇™ 의 개발자, @HackerJang(장지우) 입니다!",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "https://github.com/HackerJang",
                                        "title": "HackerJang Github"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        print('>> 애플리케이션: %s 에게 소스코드 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 소스코드를 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

    def qr_start(self, recipient_id):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": "처음 만나서 반가워요! 저는 앞으로 당신의 소중한 건강을 지켜드릴 미세봇이라고 해요! 😇",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "만나서 반가워 🤗",
                        "payload": "NICE_TO_MEET_YOU"
                    },
                    {
                        "content_type": "text",
                        "title": "더 알아볼래!",
                        "payload": "KNOW_MORE"
                    },
                    {
                        "content_type": "text",
                        "title": "🚨 버그 신고하기",
                        "payload": "BUG_REPORT"
                    }
                ]
            }
        }
        print('>> 애플리케이션: %s 에게 "Quick Reply: Start"를 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 "Quick Reply: Start"를 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

    def qr_fine_dust(self, recipient_id, gu):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": "→ " + gu + "의 미세먼지 데이터입니다. 😚",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "🚨 버그 신고하기",
                        "payload": "BUG_REPORT"
                    }
                ]
            }
        }
        print('>> 애플리케이션: %s 에게 "Quick Reply: Fine Dust" 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 "Quick Reply: Fine Dust"를 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

    def qr_know_more(self, recipient_id):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "messaging_type": "RESPONSE",
            "text": "제가 할 수 있는 것들은 이런 것들이 있어요.",
            "message": {
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "누가 만들었어?",
                        "payload": "WHO_MADE_IT"
                    },
                    {
                        "content_type": "text",
                        "title": "🚨 버그 신고하기",
                        "payload": "BUG_REPORT"
                    }
                ]
            }
        }
        print('>> 애플리케이션: %s 에게 "Quick Reply: Know More" 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 "Quick Reply: Know More"를 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

    def qr_know_me(self, recipient_id):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "messaging_type": "RESPONSE",
            "text": "만나서 반가워요! 이제 한번 제가 할 수 있는 것들에 대해 알아볼까요?",
            "message": {
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "그래!",
                        "payload": "KNOW_ME"
                    },
                    {
                        "content_type": "text",
                        "title": "🚨 버그 신고하기",
                        "payload": "BUG_REPORT"
                    }
                ]
            }
        }
        print('>> 애플리케이션: %s 에게 "Quick Reply: Know Me" 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 "Quick Reply: Know Me"를 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

    def qr_default(self, recipient_id, send_text):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "messaging_type": "RESPONSE",
            "text": send_text,
            "message": {
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "📁 소스 코드 보기",
                        "payload": "LOOK_SOURCE"
                    },
                    {
                        "content_type": "text",
                        "title": "✏️ 팁!",
                        "payload": "USAGE_TIP"
                    },
                    {
                        "content_type": "text",
                        "title": "🚨 버그 신고하기",
                        "payload": "BUG_REPORT"
                    }
                ]
            }
        }
        print('>> 애플리케이션: %s 에게 "Quick Reply: Default" 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 "Quick Reply: Default"를 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

    def get_started(self, recipient_id):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "get_started": [
                {
                    "payload": "FACEBOOK_WELCOME"
                }
            ]
        }
        print('>> 애플리케이션: %s 에게 "Get Started"을 보냅니다...' % recipient_id)
        response = requests.post(request_url, data=json.dumps(parameters), headers=headers)

        if response.status_code == 200:
            print('>> 애플리케이션: %s 에게 "Get Started"를 성공적으로 보냈습니다!' % recipient_id)

            return {
                "result": "success"
            }

    @staticmethod
    def get_user_info(user_id):
        request_url = 'https://graph.facebook.com/' + user_id + \
                      '?fields=first_name,last_name' \
                      '&access_token=' + ACCESS_TOKEN

        response = requests.get(request_url)
        result = response.json()

        if response.status_code == 200:
            return {
                "result": "success",
                "data": {
                    "first_name": result['first_name'],
                    "last_name": result['last_name']
                }
            }
        else:
            if result['error']['code'] == 10:
                # 페이지 이름으로 요청 시 Page Public Content Access 권한이 없기 때문에, 오류가 발생한다.
                return {
                    "result": "error",
                    "error": "페이지 이름으로 요청하셔서 사용자 정보를 가져올 수 없어요. - FB_PAGE",
                    "code": "FB_PAGE"
                }

            if result['error']['code'] == 803:
                # user_id가 올바르지 않다
                return {
                    "result": "error",
                    "error": "user_id가 올바르지 않아요! - FB_INVALID_USER_ID",
                    "code": "FB_INVALID_USER_ID"
                }

            else:
                # 가망이 없는 경우
                print('>> 에러! 애플리케이션 -> facebook.py -> get_user_info : FB_USER_INFO_UNKNOWN_ERROR')

                return {
                    "result": "error",
                    "error": "서버 에러가 발생했어요. 페이스북에서 사용자 정보를 가져올 수 없어요! - FB_USER_INFO_UNKNOWN_ERROR",
                    "code": "FB_USER_INFO_UNKNOWN_ERROR"
                }
