# Development Roadmap
#voice-ai #agent #architecture #mvp #security #automation

## 목적
프로토타입부터 고급 에이전트까지의 개발 단계를 실제 실행 가능한 순서로 정리한다.

## 핵심 요약
- 1단계는 기능 검증, 2단계는 제품화, 3단계 이후는 자동화와 기억 확장이다.
- 장기 메모리와 고급 에이전트는 후반 단계로 미루는 것이 안전하다.

## 상세 내용
### 1단계: 프로토타입
- 작업 내용
  - 브라우저 마이크 입력
  - STT -> LLM -> TTS 단일 턴 구현
  - 뉴스/주식 조회 도구 연결
  - Gmail draft 생성 및 승인 후 send
- 사용 기술
  - Next.js
  - FastAPI
  - OpenAI Realtime/Responses
  - Gmail API
  - Polygon/GNews
- 결과물
  - 로컬 동작 MVP

### 2단계: 웹 UI
- 작업 내용
  - transcript UI
  - approval panel
  - activity log
  - 로그인/세션 관리
- 사용 기술
  - Next.js App Router
  - TypeScript
  - Auth.js/Clerk
- 결과물
  - 사용자 테스트 가능한 웹 앱

### 3단계: 자동화 기능
- 작업 내용
  - 매일 기술 뉴스 스크럼 자동 생성
  - 정시 브리핑
  - 알림 및 webhook 연동
- 사용 기술
  - n8n
  - cron
  - Redis queue
- 결과물
  - 반자동 개인 브리핑 시스템

### 4단계: 장기 메모리
- 작업 내용
  - 사용자 선호도 저장
  - 대화/문서/뉴스 히스토리 임베딩
  - 기억 조회 정책 추가
- 사용 기술
  - PostgreSQL
  - pgvector
  - embedding pipeline
- 결과물
  - 세션을 넘는 개인화 기능

### 5단계: 앱화
- 작업 내용
  - 데스크톱 패키징
  - 파일 드래그앤드롭
  - 시스템 알림
- 사용 기술
  - Tauri 또는 Electron
- 결과물
  - 데스크톱 비서 앱

### 6단계: 고급 에이전트
- 작업 내용
  - 멀티스텝 계획
  - 승인 대기/재개
  - GitHub/캘린더/문서/파일 확장
  - 안전한 터미널/파일 도구 추가
- 사용 기술
  - LangGraph
  - Redis/Postgres persistence
  - policy engine
- 결과물
  - 승인형 실행 에이전트 플랫폼

### 단계별 진입 기준
- 2단계 전: 이메일 오발송 0건
- 3단계 전: 뉴스/주식 품질 검증
- 4단계 전: 개인정보 정책 문서화
- 6단계 전: 권한/로그/복구 정책 정립

## 관련 문서
- [[MVP_Definition]]
- [[Security_Model]]
- [[Approval_System]]
- [[Tech_Stack_Decision]]
- [[Practical_Constraints]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Scaling_Strategy]]
