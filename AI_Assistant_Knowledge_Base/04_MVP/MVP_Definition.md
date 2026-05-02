# MVP Definition
#voice-ai #agent #architecture #mvp #security #automation

## 목적
최소 제품(MVP)의 범위와 성공 기준을 명확히 정의한다.

## 핵심 요약
- MVP는 “읽기 중심 + 승인형 쓰기” 구조로 제한한다.
- 포함 기능은 `음성 입력`, `기술 뉴스 요약`, `주식 조회`, `이메일 초안 작성 + 승인 후 발송`, `음성 응답`이다.
- 핵심 성공 기준은 “똑똑함”이 아니라 “안전하고 일관된 실행”이다.

## 상세 내용
### MVP 포함 기능
1. 음성 입력
2. 기술 뉴스 요약
3. 주식 조회
4. 이메일 초안 작성 + 승인 후 발송
5. 음성 응답

### MVP 비포함 기능
- OS 전체 제어
- 자동 메일 발송 without approval
- 파일 삭제/수정
- 터미널 명령 자동 실행
- 고도 장기 메모리
- IoT 제어
- 멀티 사용자 조직 기능

### MVP 제품 정의
MVP는 다음과 같은 제품이다.
- 브라우저에서 사용하는 음성 비서
- 특정 정보 조회와 제한된 생산성 작업 실행
- 승인 후에만 쓰기 작업을 수행
- 실행 이력과 승인 이력을 저장

### 성공 기준
- 음성 입력 후 응답까지 지연이 실사용 가능 수준일 것
- 이메일 발송 전 100% 승인 요구
- 기술 뉴스 요약에 출처 링크 포함
- 주식 응답에 가격/변동/뉴스를 함께 제공
- 실행 로그와 승인 로그가 남을 것

### MVP에서 중요한 UX 요소
- Push-to-talk 또는 실시간 음성 버튼
- transcript 패널
- 실행 예정 액션 카드
- 승인/수정/거절 인터페이스
- 결과 요약 카드

## 관련 문서
- [[User_Flows]]
- [[Feature_Difficulty_Table]]
- [[System_Architecture]]
- [[Security_Model]]
- [[Tech_Stack_Decision]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Project_Structure]]
