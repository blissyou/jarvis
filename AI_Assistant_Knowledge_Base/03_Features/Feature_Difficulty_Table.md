# Feature Difficulty Table
#voice-ai #agent #architecture #mvp #security #automation

## 목적
각 기능의 구현 가능성, 난이도, 필요한 도구, 위험 요소, MVP 포함 여부를 표로 관리한다.

## 핵심 요약
- MVP에는 음성, 기술 뉴스, 주식, 이메일 초안/승인 발송만 포함하는 것이 적절하다.
- 캘린더, GitHub 보조, 문서 요약은 2차 이후가 적합하다.
- 터미널, 파일 수정, IoT는 고위험 확장 영역이다.

## 상세 내용
| 기능 | 구현 가능성 | 난이도 | 필요한 API/도구 | 위험 요소 | MVP 포함 여부 |
|---|---|---|---|---|---|
| 음성 명령 STT | 높음 | 중 | OpenAI Realtime, Deepgram | 잡음, 지연, 한국어 품질 | 포함 |
| 자연어 의도 파악 | 높음 | 중 | OpenAI Responses/Reatime | 잘못된 tool 선택 | 포함 |
| 추가 질문 | 높음 | 중 | LLM + 세션 상태 | 질문 과잉, 슬롯 누락 | 포함 |
| 음성 응답 TTS | 높음 | 하 | OpenAI TTS, Azure Speech | 음성 품질, 지연 | 포함 |
| 관심 종목 현재가 조회 | 높음 | 하 | Polygon/Finnhub | 실시간 데이터 요금제 | 포함 |
| 주가 변동 요약 | 높음 | 중 | Stock API + LLM | 과장 요약, 지연 데이터 | 포함 |
| 관련 뉴스 요약 | 높음 | 중 | GNews/NewsAPI + LLM | 출처 품질, 중복 기사 | 포함 |
| 개발 뉴스 스크럼 | 높음 | 중 | GNews/RSS + cron + LLM | 소스 편향, 중복 | 포함 |
| 이메일 초안 작성 | 높음 | 중 | Gmail drafts.create | 잘못된 수신자 | 포함 |
| 승인 후 이메일 발송 | 높음 | 중 | Gmail drafts.send | 오발송 | 포함 |
| 일정 추가 | 높음 | 중 | Google Calendar API | 시간대/날짜 오해 | 제외 |
| 리마인더 생성 | 중간 | 중 | Calendar/Tasks/자체 DB | 알림 누락 | 제외 |
| GitHub 이슈/PR 요약 | 높음 | 중 | GitHub API | private 권한 | 제외 |
| 코드 에러 분석 | 높음 | 중 | 로그/문서 업로드 + LLM | 민감 코드 노출 | 제외 |
| 터미널 명령 추천 | 높음 | 하 | LLM | 위험 명령 추천 | 제외 |
| 파일 검색/요약 | 높음 | 중 | 로컬 인덱스 + 파서 | 민감 정보 노출 | 제외 |
| IoT 제어 | 중간 | 상 | MQTT/Home Assistant | 실제 장치 오작동 | 제외 |

### 우선순위 해석
- P0: 음성, 뉴스, 주식, 이메일 승인 발송
- P1: 캘린더, GitHub, 문서 요약
- P2: 파일 조작, 터미널, IoT

## 관련 문서
- [[Feature_List]]
- [[MVP_Definition]]
- [[Security_Model]]
- [[Development_Roadmap]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Scaling_Strategy]]
