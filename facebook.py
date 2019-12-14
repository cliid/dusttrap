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
                                "image_url": "https://image.flaticon.com/icons/png/512/875/875220.png",
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

    def qr_start(self, recipient_id):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": "처음 만나서 반가워요! 저는 앞으로 당신의 소중한 호흡기를 지켜드릴 미세봇이라고 해요! 😇",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "만나서 반가워 🤗",
                        "payload": "FACEBOOK_WELCOME"
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

    def qr_fine_dust(self, recipient_id):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type': 'application/json'}
        parameters = {
            "recipient": {
                "id": recipient_id
            },
            "messaging_type": "RESPONSE",
            "message": {
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
            "message": {
                "text": "미세봇™ 은 @HackerJang(장지우)가 만든 미세먼지 실시간 확인 페메봇입니다! 🧐",
                "quick_replies": [
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
