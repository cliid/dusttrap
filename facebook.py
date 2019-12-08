import requests
import json

from key import ACCESS_TOKEN


class FacebookMessenger:
    GRAPH_URL = 'https://graph.facebook.com/v3.3/me/messages?access_token='

    def send_text_message(self, recipient_id, string):
        request_url = self.GRAPH_URL + ACCESS_TOKEN
        headers = {'content-type':  'application/json'}
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