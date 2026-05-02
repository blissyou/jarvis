# Practical Constraints
#voice-ai #agent #architecture #mvp #security #automation

## 목적
실제 개발 시 부딪히는 운영적·기술적 제약을 별도 문서로 정리한다.

## 핵심 요약
- 이 프로젝트의 병목은 모델 성능보다 범위 관리, 보안 정책, 외부 API 운영 복잡도다.
- MVP에서는 기능보다 제약을 먼저 정의해야 실패 확률이 낮아진다.

## 상세 내용
### 현실 제약
- STT 전사 품질은 환경 소음과 발화 습관에 영향을 받는다.
- 실시간 주식 데이터는 요금제 제약이 있다.
- 뉴스 API는 중복 기사와 제한된 호출량 문제가 있다.
- 이메일 발송은 OAuth와 계정 권한 설계가 필요하다.
- 장기 메모리는 비용과 개인정보 관리 이슈가 크다.
- 멀티플랫폼은 유지보수 비용이 빠르게 증가한다.

### 초기 범위에서 피해야 할 것
- 무승인 발송
- 자동 파일 수정/삭제
- 터미널 자동 실행
- 장기 메모리 중심 설계
- 복수 외부 자동화 시스템 동시 도입
- 모바일/데스크톱/웹 동시 시작

### 권장 저장소 구조 예시
```bash
jarvis/
├── web/
├── api/
├── worker/
├── infra/
├── scripts/
├── docs/
├── .env.example
└── docker-compose.yml
```

### CLI 관리 메모
```bash
mkdir -p AI_Assistant_Knowledge_Base/{00_Index,01_Research,02_Architecture,03_Features,04_MVP,05_Security,06_Roadmap,07_Tech_Stack,08_Implementation_Notes,99_References}
find . -maxdepth 2 -type f | sort
grep -R "\[\[" .
```

### 구현 우선순위 원칙
- 먼저 읽기 기능
- 그 다음 승인형 쓰기 기능
- 그 다음 스케줄링
- 마지막에 장기 메모리와 고급 에이전트

## 관련 문서
- [[Feasibility]]
- [[MVP_Definition]]
- [[Security_Model]]
- [[Development_Roadmap]]
- [[Tech_Stack_Decision]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Docker_Isolation_Strategy]]
