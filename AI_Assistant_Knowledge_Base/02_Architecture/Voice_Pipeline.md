# Voice Pipeline
#voice-ai #agent #architecture #mvp #security #automation

## 목적
음성 입력과 음성 출력 경로를 별도 책임 문서로 정리한다.

## 핵심 요약
- MVP에서는 OpenAI Realtime API 또는 STT + LLM + TTS 조합이 가장 실용적이다.
- 음성 파이프라인의 핵심은 단순한 STT 정확도보다 `낮은 지연`, `turn detection`, `후속 질문`, `응답 안정성`이다.
- 웹 브라우저가 가장 현실적인 시작점이다.

## 상세 내용
### 입력 파이프라인 후보
| 후보 | 장점 | 단점 | 추천도 |
|---|---|---|---|
| OpenAI Realtime speech-to-speech | 저지연, 함수 호출 연결이 쉬움 | 벤더 종속 | 매우 높음 |
| OpenAI Realtime transcription | 전사 전용 구조가 명확 | 대화 흐름은 별도 설계 필요 | 높음 |
| OpenAI `gpt-4o-transcribe` 계열 | 같은 공급자 체인 구성 가능 | 고도 튜닝은 제한적 | 높음 |
| Deepgram Flux/Nova | 실시간 STT와 turn detection 강점 | 공급자 추가 관리 | 높음 |
| Whisper self-host | 로컬 제어 가능 | 운영 부담과 지연 | 낮음 |

### 출력 파이프라인 후보
| 후보 | 장점 | 단점 | 추천도 |
|---|---|---|---|
| OpenAI `gpt-4o-mini-tts` | 자연스러운 음성, 스트리밍 가능 | 음성 커스텀 제한 | 매우 높음 |
| OpenAI Realtime speech output | 대화 지연 최소화 | Realtime 세션 설계 필요 | 매우 높음 |
| Azure Speech | 언어/음성 옵션 풍부 | 별도 벤더 관리 | 높음 |
| Deepgram Aura | 음성 스택 통합 가능 | 추가 운영 요소 | 중간 |

### 음성 설계 시 고려사항
- microphone noise
- VAD 설정
- turn interruption
- partial transcript 처리
- “사용자 말 끊기” 시 응답 중단
- 한국어 발음 품질
- 도구 실행 직전 confirmation prompt
- AI 음성임을 고지하는 UX

### 웹 우선 이유
- 브라우저 마이크 접근이 가장 쉽다.
- WebRTC를 활용하기 좋다.
- 실시간 transcript와 approval UI를 한 화면에 넣기 쉽다.
- MVP 검증 속도가 가장 빠르다.

## 관련 문서
- [[System_Architecture]]
- [[Tool_Execution_Model]]
- [[MVP_Definition]]
- [[User_Flows]]
- [[Tech_Stack_Decision]]

## 참고 자료
- [[References]]
> [!warning] Deprecated  
> Superseded by: [[Execution_Flows]]
