# User Flows
#voice-ai #agent #architecture #mvp #security #automation

## 목적
MVP에 포함되는 핵심 사용자 시나리오를 단계별 흐름으로 정리한다.

## 핵심 요약
- 뉴스, 주식, 이메일은 각각 다른 위험도와 UI 요구사항을 가진다.
- 이메일은 승인 중심 플로우이고, 뉴스와 주식은 읽기 중심 플로우다.

## 상세 내용
### 1. 기술 뉴스 스크럼 플로우
```text
사용자 음성 입력
-> STT
-> "오늘 개발 뉴스 요약해줘" 의도 인식
-> 뉴스 API/RSS 수집
-> AI/임베디드/웹/C#/Docker/Linux/GitHub 필터링
-> 중복 제거
-> 한국어 핵심 요약 생성
-> 출처 링크 포함
-> TTS 응답
```

### 2. 주식 브리핑 플로우
```text
"엔비디아랑 테슬라 오늘 어때?"
-> 종목명/티커 추출
-> 현재가 / 전일 대비 / 변동률 조회
-> 관련 뉴스 수집
-> 정보 제공 중심 요약 생성
-> 투자 조언이 아님을 명시
-> TTS 응답
```

### 3. 이메일 초안/승인/발송 플로우
```text
"김철수에게 내일 회의 연기 메일 써줘"
-> 수신자 / 제목 / 본문 초안 생성
-> 누락 정보 확인
-> Gmail draft 생성
-> UI 미리보기 표시
-> 사용자 승인 또는 수정
-> drafts.send 실행
-> 발송 완료 응답
```

### 4. 승인 UX 요구사항
- 액션 이름 표시
- 대상 수신자 또는 리소스 표시
- 입력 파라미터 표시
- 승인/수정/취소 버튼
- 실행 후 결과 표시

### 5. 예외 처리 포인트
- STT 전사 오류
- 종목명 인식 실패
- 이메일 주소 누락
- API rate limit
- 뉴스 결과 없음
- 사용자가 승인 거절

## 관련 문서
- [[MVP_Definition]]
- [[Voice_Pipeline]]
- [[Tool_Execution_Model]]
- [[Approval_System]]
- [[Security_Model]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Execution_Flows]]
