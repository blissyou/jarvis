# Security Model
#voice-ai #agent #architecture #mvp #security #automation

## 목적
프로젝트 전반의 보안 원칙, 위험 분류, 권한 모델을 정의한다.

## 핵심 요약
- 이 시스템의 가장 큰 위험은 “잘못된 실행”이다.
- 따라서 tool별 위험도 분류, 사용자 승인, API 키 보호, 권한 분리, 실행 로그가 필수다.
- 로컬 vs 클라우드는 이분법이 아니라 데이터와 권한의 분리 설계 문제다.

## 상세 내용
### 위험 분석 표
| 영역 | 주요 위험 | 대응 |
|---|---|---|
| 이메일 | 오발송, 잘못된 수신자, 피싱성 응답 | draft 우선, 승인 필수, 화이트리스트 |
| 파일 접근 | 민감 파일 노출, 잘못된 수정/삭제 | 샌드박스 루트, read/write 분리 |
| 터미널 실행 | 파괴적 명령, 정보 유출 | 기본 비활성, allowlist |
| 주식 정보 | 투자 조언으로 오해 | 정보 제공 고지 |
| 뉴스 요약 | 왜곡, 저작권 문제 | 링크 제공, 과도한 본문 인용 금지 |
| 장기 메모리 | 개인정보 과잉 축적 | opt-in, TTL, 삭제 정책 |

### API Key 관리
- 클라이언트에 provider secret 직접 노출 금지
- 서버에서만 장기 키 보관
- 브라우저에는 ephemeral/session token만 전달
- 환경 변수 또는 secret manager 사용
- 서비스별 키 분리

### 로컬 vs 클라우드 판단
| 기준 | 로컬 우선 | 클라우드 우선 |
|---|---|---|
| 개인정보 | 유리 | 불리 |
| 개발 속도 | 느림 | 빠름 |
| 운영 복잡도 | 높음 | 중간 |
| 품질 | 직접 튜닝 필요 | 상용 API 품질 활용 |
| 비용 구조 | 인프라 선투자 | 사용량 기반 |

### 권장 보안 원칙
- 쓰기 도구는 기본적으로 승인 필요
- 관리자 도구는 기본 비활성
- 세션/로그에서 PII 최소 저장
- 사용자별 연결 계정 분리
- 모든 실행에 trace ID 기록

## 관련 문서
- [[Approval_System]]
- [[Tool_Execution_Model]]
- [[Practical_Constraints]]
- [[MVP_Definition]]
- [[Tech_Stack_Decision]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Security/Security_Model|Security_Model]]
