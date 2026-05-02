# Approval System
#voice-ai #agent #architecture #mvp #security #automation

## 목적
사용자 승인 구조를 별도 문서로 정의하여 안전한 실행 정책의 중심축으로 사용한다.

## 핵심 요약
- 승인 시스템은 이 프로젝트의 핵심 안전장치다.
- 모든 도구를 `read-only`, `confirm-required`, `admin-only`로 구분한다.
- 특히 이메일, 파일 수정, 일정 생성, 터미널, IoT는 승인 흐름 없이는 실행하면 안 된다.

## 상세 내용
### 권한 분류 모델
#### 1. Read-only
- 뉴스 조회
- 주식 조회
- GitHub 읽기
- 캘린더 조회
- 문서 요약

#### 2. Confirm-required
- 이메일 발송
- 일정 생성
- 리마인더 생성
- 파일 수정
- 외부 webhook 호출

#### 3. Admin-only / Disabled by default
- 터미널 실행
- 파일 삭제
- 시스템 설정 변경
- IoT 제어

### 승인 흐름
1. LLM이 tool call 생성
2. 정책 엔진이 위험도 판단
3. confirm-required 이상이면 실행 중단
4. 사용자에게 preview card 표시
5. 승인 / 수정 / 거절 중 선택
6. 승인 후 실행
7. 결과 저장

### 승인 UI 필수 요소
- 도구 이름
- 대상 리소스
- 실행 인자
- 예상 결과
- 승인/수정/거절 버튼
- 로그 기록

### 승인 시스템이 필요한 이유
- LLM 환각 가능성
- 사용자의 모호한 발화
- STT 오인식
- 돌이킬 수 없는 외부 작업 존재
- 계정/개인정보 관련 위험

## 관련 문서
- [[Security_Model]]
- [[Tool_Execution_Model]]
- [[User_Flows]]
- [[MVP_Definition]]
- [[Development_Roadmap]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Permission_and_Approval_Model]]
