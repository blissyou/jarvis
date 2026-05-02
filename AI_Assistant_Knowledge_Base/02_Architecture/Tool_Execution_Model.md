# Tool Execution Model
#voice-ai #agent #architecture #mvp #security #automation

## 목적
LLM이 실제 도구를 어떻게 호출하고, 서버가 어떻게 안전하게 실행하는지 모델을 정의한다.

## 핵심 요약
- 초기 구현은 function calling 기반 tool router가 가장 단순하고 안정적이다.
- 복잡한 멀티스텝 자동화는 LangGraph와 n8n으로 확장하는 하이브리드 모델이 적합하다.
- 핵심 설계 포인트는 도구의 수가 아니라 `도구 실행 정책과 승인 구조`다.

## 상세 내용
### 기본 실행 흐름
1. 사용자의 발화 또는 텍스트 입력 수신
2. LLM이 intent와 필요한 tool call 생성
3. 서버가 tool schema 검증
4. 정책 엔진이 승인 필요 여부 판단
5. 승인 필요 시 실행 중단 및 사용자 확인
6. 승인 후 tool executor가 실제 API 호출
7. 결과를 다시 LLM에 전달
8. 자연어/음성 응답 생성

### 도구 실행 방식 비교
| 방식 | 사용 시점 | 장점 | 단점 |
|---|---|---|---|
| 직접 API 호출 | Gmail, Calendar, GitHub, Stock, News | 예측 가능, 추적 쉬움 | 구현량 증가 |
| Python 함수 | 파싱, 전처리, 검색 | AI 백엔드와 궁합 좋음 | 서버 코드 관리 필요 |
| Webhook | 외부 자동화, n8n | 유연함 | 흐름 추적 분산 |
| LangGraph | 멀티스텝 승인형 실행 | pause/resume, 상태 관리 | 초기 복잡도 있음 |
| n8n | cron, 반복 자동화, 알림 | 비개발 워크플로에 좋음 | 핵심 에이전트로는 제한적 |

### 권장 단계별 모델
#### 1단계
- OpenAI Responses API function calling
- 서버 측 tool router
- Gmail/Stock/News 정도만 연결

#### 2단계
- approval interrupt
- 실행 로그
- 실패 재시도
- 입력 검증 강화

#### 3단계
- LangGraph stateful agent
- long-running task
- human-in-the-loop
- pause/resume

#### 4단계
- n8n을 스케줄링과 외부 자동화로 연결

### 도구 설계 원칙
- tool description은 명확하고 짧게 유지
- 입력 파라미터는 JSON schema로 강제
- tool은 read/write/admin 범주로 분류
- 이메일, 파일, 일정, 터미널은 고위험으로 분류
- tool output은 가능한 구조화된 JSON으로 반환

## 관련 문서
- [[System_Architecture]]
- [[Security_Model]]
- [[Approval_System]]
- [[User_Flows]]
- [[Tech_Stack_Decision]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Tool_Invocation_Model]]
