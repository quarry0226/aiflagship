import logging
import time

import sys


#from __future__ import print_function
import datetime
from datetime import timedelta 
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


from event import ChatMessageEvent, UserDropEvent, UserPasswordChangedEvent, ChatInitEvent
from thread_pool import ThreadPool

logger = logging.getLogger("teamup-bot")
SCOPES = 'https://www.googleapis.com/auth/calendar'

class BaseBot:
    def __init__(self, service):
        self.service = service
        self.error_count = 0
        self.thread_pool = ThreadPool()

    # thread-safe 하다고 나와있긴 하지만 보장이 되는지 고민해 봐야함
    # callback 패턴으로 바꾸는 것 고려
    def handle_event(self, events):
        for event in events:
            if isinstance(event, ChatInitEvent):
                #print(event.user_index)
                self.handle_entered_room(event.team_index, event.room_index)

            elif isinstance(event, ChatMessageEvent):
                chat = self.service.get_chat_summary(event.room_index,
                                                     event.msg_index)
                if chat:
                    self.handle_chat(event.team_index, event.room_index, chat)

            elif isinstance(event, UserDropEvent) \
                    and self.service.my_index == event.user_index:
                logger.error("봇 계정이 탈퇴되었습니다.")
                sys.exit()
            elif isinstance(event, UserPasswordChangedEvent) \
                    and self.service.my_index == event.user_index:
                logger.error("봇 계정의 비밀번호가 바뀌었습니다.")
                sys.exit()

    def run(self):
        while True:
            try:
                events = self.service.get_events()
                if events:
                    self.thread_pool.add_task(self.handle_event, events)
                time.sleep(self.service.config['lp_idle_time'])
            except Exception as e:
                self.error_count += 1
                if self.error_count > 3:
                    logger.error("오류가 발생했습니다. 프로그램을 종료합니다.")
                    #sys.exit()
                else:
                    logger.error("오류가 발생했습니다.:"+e)
                    time.sleep(5)

    def handle_entered_room(self, team_index, room_index):
        raise NotImplementedError()

    def handle_chat(self, team_index, room_index, chat):
        raise NotImplementedError()


def run_flow(flow, storage, flags=None, http=None):
    if flags is None:
        flags = argparser.parse_args()
    logging.getLogger().setLevel(getattr(logging, flags.logging_level))
    if not flags.noauth_local_webserver:
        success = False
        port_number = 0
        for port in flags.auth_host_port:
            port_number = port
            try:
                httpd = ClientRedirectServer((flags.auth_host_name, port),
                                             ClientRedirectHandler)
            except socket.error:
                pass
            else:
                success = True
                break
        flags.noauth_local_webserver = not success
        if not success:
            print(_FAILED_START_MESSAGE)

    if not flags.noauth_local_webserver:
        oauth_callback = 'http://{host}:{port}/'.format(
            host=flags.auth_host_name, port=port_number)
    else:
        oauth_callback = client.OOB_CALLBACK_URN
    flow.redirect_uri = oauth_callback
    authorize_url = flow.step1_get_authorize_url()

    if not flags.noauth_local_webserver:
        import webbrowser
        webbrowser.open(authorize_url, new=1, autoraise=True)
        print(_BROWSER_OPENED_MESSAGE.format(address=authorize_url))
    else:
        print(_GO_TO_LINK_MESSAGE.format(address=authorize_url))

    code = None
    if not flags.noauth_local_webserver:
        httpd.handle_request()
        if 'error' in httpd.query_params:
            sys.exit('Authentication request was rejected.')
        if 'code' in httpd.query_params:
            code = httpd.query_params['code']
        else:
            print('Failed to find "code" in the query parameters '
                  'of the redirect.')
            sys.exit('Try running with --noauth_local_webserver.')
    else:
        code = input('Enter verification code: ').strip()

    try:
        credential = flow.step2_exchange(code, http=http)
    except client.FlowExchangeError as e:
        sys.exit('Authentication has failed: {0}'.format(e))

    storage.put(credential)
    credential.set_store(storage)
    print('Authentication successful.')

    return credential


################### KAIST by quarry@kaist.ac.kr(Lee Chae Seok)############################
class KAISTBot(BaseBot):
    def handle_entered_room(self, team_index, room_index):
        #print(str(team_index)+","+str(room_index))
        chat_user_index = self.service.get_my_room_info(room_index)
        print(chat_user_index)
        chat_user_info = self.service.get_chat_user_info(chat_user_index, team_index)
        print(chat_user_info)

        self.service.post_chat(team_index, room_index, "안녕하세요. "+chat_user_info['name']+"님. 저는 KAIST 봇입니다.")

    def handle_chat(self, team_index, room_index, chat):
        if chat and chat.content == "Hello":
            self.service.post_chat(team_index, room_index, "World")

        elif chat and chat.content == "cal":
            """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
            """
            store = file.Storage('token.json')
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
                flow.redirect_uri = 'http://localhost'
                authorize_url = flow.step1_get_authorize_url()
                self.service.post_chat(team_index, room_index, authorize_url)
                creds = tools.run_flow(flow, store)                
         
            service = build('calendar', 'v3', http=creds.authorize(Http()))

            now = datetime.datetime.utcnow()

            current_time = now.isoformat() + 'Z' # 'Z' indicates UTC time

            #시간 유동적으로 추가 변환 하는 부분. 현재는 +30분
            etime = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            event_time = etime.isoformat() + 'Z'

            #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            #event_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
            #event_time = str(event_time) + 'Z' # 'Z' indicates UTC time

            # 이벤트 한개 추가
            event = {
              "summary": "Test AIF",
              "description": "이 부분에 솔루션이 기록 됩니다. 포맷 및 형식 정의 필요.",
              'start': {
                'dateTime': current_time,
                'timeZone': 'Asia/Seoul',
              },
              'end': {
                'dateTime': event_time,
                'timeZone': 'Asia/Seoul',
              },
            }

            events_result = service.events().insert(calendarId='43qnadjcam3os9fuvlnaqegl48@group.calendar.google.com', body=event).execute()

            #현재 시간에서부터 향후 10개까지의 이벤트를 출력
            print('Getting the upcoming 10 events')

            events_result = service.events().list(calendarId='43qnadjcam3os9fuvlnaqegl48@group.calendar.google.com', timeMin=current_time,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            #이벤트 출력
            if not events:
                print('No upcoming events found.')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

            #현재 시간에서부터 향후 10개까지의 이벤트를 출력
        #    events_result = service.events().list(calendarId='43qnadjcam3os9fuvlnaqegl48@group.calendar.google.com', timeMin=now,
        #                                        maxResults=10).execute()
        #    events = events_result.get('items', [])

            #이벤트 출력
        #    if not events:
        #        print('No upcoming events found.')
        #    for event in events:
        #        print(event)
                #start = event['start'].get('dateTime', event['start'].get('date'))
                #print(start, event['summary'])
            self.service.post_chat(team_index, room_index, "캘린더 추가")
            
        
        else : #loopback
            self.service.post_chat(team_index, room_index, "loopback:"+chat.content, 0)



################# estsoft examples, as seen. ############################

class TextBot(BaseBot):
    def handle_entered_room(self, team_index, room_index):
        self.service.post_chat(team_index, room_index, "안녕하세요. 저는 샘플 봇입니다.")

    def handle_chat(self, team_index, room_index, chat):
        if chat and chat.content == "Hello":
            self.service.post_chat(team_index, room_index, "World")


class ButtonBot(BaseBot):
    def __init__(self, service):
        super(ButtonBot, self).__init__(service)
        self.buttons = [
            {"type": "text", "id": "bottom", "button_text": "하단 버튼 예시", "response_text": "하단 버튼을 보여주세요."},
            {"type": "text", "id": "calendar_button", "button_text": "달력 예시", "response_text": "달력을 보여주세요."},
            {"type": "text", "id": "range_calendar_button", "button_text": "범위 달력 예시", "response_text": "범위 달력을 보여주세요."}
        ]
        self.test_extras = {
            "2": {
                'type': 'bot',
                'message_buttons': [
                    {"type": "url", "button_text": "팀업 홈페이지", "url": "https://tmup.com"},
                    {"type": "url", "button_text": "챗봇 가이드 문서",
                     "url": "http://cf-xdn.altools.co.kr/teamUP/TeamUP_develop_chatbot_guide_v2.pdf"}
                ],
                'scroll_buttons': self.buttons
            }
        }

    def handle_entered_room(self, team_index, room_index):
        self.service.post_chat(team_index, room_index, "안녕하세요. 저는 샘플 봇입니다.", self.test_extras)

    def handle_chat(self, team_index, room_index, chat):
        if chat.content == "?":
            self.service.post_chat(team_index, room_index, "안녕하세요. 저는 샘플 봇입니다.", self.test_extras)

        elif chat.response_id == "bottom":
            extras = {
                "2": {
                    'type': 'bot',
                    'bottom': {
                        'type': 'button',
                        'buttons': self.buttons
                    }
                }
            }
            self.service.post_chat(team_index, room_index, "하단 버튼을 보여드리겠습니다.", extras)

        elif chat.response_id == "calendar_button":
            extras = {
                "2": {
                    'type': 'bot',
                    'bottom': {
                        'id': 'test_calendar',
                        'type': 'calendar',
                        'range': False
                    }
                }
            }

            self.service.post_chat(team_index, room_index, "달력을 보여드리겠습니다.", extras)

        elif chat.response_id == "range_calendar_button":
            extras = {
                "2": {
                    'type': 'bot',
                    'bottom': {
                        'id': 'test_range_calendar',
                        'type': 'calendar',
                        'range': True
                    }
                }
            }

            self.service.post_chat(team_index, room_index, "범위 달력을 보여드리겠습니다.", extras)

        elif chat.response_id == "test_calendar":
            extras = {
                "2": {
                    'type': 'bot',
                    'scroll_buttons': self.buttons
                }
            }
            self.service.post_chat(team_index, room_index, "{} 날짜를 선택해 주셨네요.".format(chat.content), extras)

        elif chat.response_id == "test_range_calendar":
            extras = {
                "2": {
                    'type': 'bot',
                    'scroll_buttons': self.buttons
                }
            }
            split_result = chat.content.split("~")
            range_start = split_result[0]
            range_end = split_result[1]
            content = "{} 부터 {} 날짜를 선택해 주셨네요.".format(range_start, range_end)
            self.service.post_chat(team_index, room_index, content, extras)
