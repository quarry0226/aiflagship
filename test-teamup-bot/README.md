# 현재 테스트 버전이니 사용하지 마시길 바람

# KAIST Integration Server v0.1
- Python teamup bot client
- KAIST Bot을 위한 Integration 시스템 추가 (quarry@kaist.ac.kr)

## 프로젝트 설정
디렉토리에서 requirements 설치
```
pip install -r requirements.txt
```

### configuration.json 포맷
```
{
  "client_id": "Your client id",
  "client_secret": "Your client secret",
  "username": "your@email.com",
  "password": "yourpwd",
  "button_bot": false
}
```

client id / client secret 발급 문의 (https://tmup.com/main/developer)

## 실행(2개의 프로그램 실행해야 함)
main.py 실행
/tossBot/tossChatDataServer.py 실행 (새창을 열어서)


## api reference
- http://team-up.github.io/
