# Feature List
#voice-ai #agent #architecture #mvp #security #automation

## 목적
프로젝트 범위 안의 기능들을 명확하게 카테고리별로 정리한다.

## 핵심 요약
- 기능은 음성 인터페이스, 정보 조회, 커뮤니케이션, 일정/작업 관리, 개발 보조, 확장 기능으로 나뉜다.
- 초기 설계는 “읽기 기능 중심 + 승인형 쓰기 기능”으로 구성하는 것이 안전하다.

## 상세 내용
### 1. 음성 인터페이스
- 마이크 입력 수집
- STT
- 자연어 명령 이해
- 추가 질문
- TTS 응답

### 2. 주식 기능
- 관심 종목 현재가 조회
- 전일 대비/변동률 요약
- 관련 뉴스 수집 및 요약
- 투자 조언이 아닌 정보 제공 중심 응답

### 3. 개발 기사 / 기술 뉴스 스크럼
- AI
- 임베디드
- 웹
- C#
- Docker
- Linux
- GitHub
- 한국어 요약
- 출처 링크 포함

### 4. 이메일 기능
- 음성으로 이메일 작성
- 수신자/제목/본문 구조화
- 초안 생성
- 발송 전 승인
- 승인 후 발송

### 5. 일정 / 할 일
- 캘린더 일정 추가
- 리마인더 생성
- 오늘 할 일 요약

### 6. 개발 보조
- GitHub 이슈/PR 요약
- 코드 에러 분석
- 터미널 명령 추천
- 프로젝트 문서 요약

### 7. 확장 기능
- 날씨
- 일반 뉴스
- 파일 검색
- 웹 검색
- 문서 요약
- 알림
- IoT 제어 가능성 검토

### 기능 분류 관점
- Read-heavy: 뉴스, 주식, GitHub 읽기, 문서 요약
- Write-heavy: 이메일 발송, 일정 등록, 파일 수정
- High-risk: 터미널 실행, 파일 삭제, IoT 제어

## 관련 문서
- [[Feature_Difficulty_Table]]
- [[MVP_Definition]]
- [[Security_Model]]
- [[Approval_System]]
- [[Development_Roadmap]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Developer_Workflows]]
