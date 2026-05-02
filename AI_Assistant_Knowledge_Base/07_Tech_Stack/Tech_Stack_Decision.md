# Tech Stack Decision
#voice-ai #agent #architecture #mvp #security #automation

## 목적
Python과 Node.js를 포함한 실제 구현 기술 스택을 비교하고 최종 권장 조합을 정의한다.

## 핵심 요약
- 단일 언어보다 `Next.js + FastAPI` 이원 구조가 가장 현실적이다.
- Python은 AI/데이터/도구 실행에 강하고, Node.js는 웹 UI와 실시간 브라우저 경험에 강하다.
- Docker 기반 `web`, `api`, `worker`, `db`, `redis` 구성이 확장성 면에서 적합하다.

## 상세 내용
### Python vs Node.js 비교
| 기준 | Python | Node.js |
|---|---|---|
| AI 라이브러리 | 매우 강함 | 보통 |
| 문서 파싱/데이터 처리 | 매우 강함 | 중간 |
| LangGraph/LangChain | 주력 생태계 | 사용 가능 |
| 브라우저 실시간 SDK/WebRTC | 중간 | 강함 |
| 프론트엔드 통합 | 약함 | 매우 강함 |
| 풀스택 개발 속도 | 중간 | 높음 |

### 권장 역할 분리
- `Next.js`
  - 웹 UI
  - 마이크 인터페이스
  - transcript
  - approval panel
  - session UX
- `FastAPI`
  - agent backend
  - tool orchestration
  - policy engine
  - scheduler API
  - persistence control

### 추천 스택
| 영역 | 추천 |
|---|---|
| 프론트엔드 | Next.js 16 + TypeScript |
| 백엔드 API | FastAPI + Pydantic |
| 에이전트 | OpenAI Responses API -> 이후 LangGraph 확장 |
| 실시간 음성 | OpenAI Realtime API |
| STT 대안 | Deepgram |
| TTS 대안 | Azure Speech |
| DB | PostgreSQL |
| Vector | pgvector |
| Cache/Queue | Redis |
| 자동화 | n8n |
| 인증 | Google OAuth + Auth.js/Clerk |
| 배포 | Docker Compose |
| 모니터링 | Sentry + OpenTelemetry |

### Docker 기반 기본 구성
```yaml
services:
  web:
    build: ./web
  api:
    build: ./api
  worker:
    build: ./api
  db:
    image: postgres:17
  redis:
    image: redis:8
```

### 최종 권장 조합
- Frontend: Next.js
- Backend: FastAPI
- LLM/Voice: OpenAI
- Workflow: 초기 function calling, 이후 LangGraph
- Automation: n8n 보조
- Storage: PostgreSQL + pgvector + Redis
- Infra: Docker Compose

## 관련 문서
- [[System_Architecture]]
- [[Voice_Pipeline]]
- [[Tool_Execution_Model]]
- [[MVP_Definition]]
- [[Practical_Constraints]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[ADR_003_Open_Interpreter_and_MCP]]
