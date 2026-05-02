# References
#voice-ai #agent #architecture #mvp #security #automation

## 목적
이 Knowledge Base 전반에서 사용한 주요 참고 자료를 한곳에 정리한다.

## 핵심 요약
- 가능성 검증과 설계 판단은 공식 문서와 1차 출처 중심으로 수행했다.
- 음성/에이전트는 OpenAI, 오케스트레이션은 LangGraph/n8n, 생산성 도구는 Google/GitHub, 데이터 저장은 FastAPI/pgvector/Redis, 외부 데이터는 Polygon/GNews를 기준으로 삼았다.

## 상세 내용
### OpenAI
- Realtime API Voice Design  
  https://platform.openai.com/docs/guides/realtime/voice-design
- Realtime WebRTC  
  https://platform.openai.com/docs/guides/realtime-webrtc
- Realtime Transcription  
  https://platform.openai.com/docs/guides/realtime-transcription
- Function Calling  
  https://platform.openai.com/docs/guides/function-calling
- Agents SDK  
  https://platform.openai.com/docs/guides/agents-sdk/
- Text-to-Speech  
  https://platform.openai.com/docs/guides/text-to-speech
- Assistants Function Calling Deprecation  
  https://platform.openai.com/docs/assistants/tools/function-calling

### Google
- Gmail Sending  
  https://developers.google.com/workspace/gmail/api/guides/sending
- Gmail Drafts  
  https://developers.google.com/workspace/gmail/api/guides/drafts
- Google Calendar Create Events  
  https://developers.google.com/workspace/calendar/api/guides/create-events

### LangChain / LangGraph / n8n
- LangGraph Overview  
  https://docs.langchain.com/oss/python/langgraph/overview
- Human-in-the-Loop  
  https://docs.langchain.com/oss/python/langchain/human-in-the-loop
- n8n AI Agent Node  
  https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
- n8n Agents Overview  
  https://docs.n8n.io/advanced-ai/examples/understand-agents/
- n8n OpenAI Functions Agent  
  https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/openai-functions-agent/

### Web / Backend / Data
- FastAPI  
  https://fastapi.tiangolo.com/
- FastAPI Tutorial  
  https://fastapi.tiangolo.com/tutorial/
- Next.js App Router  
  https://nextjs.org/docs/app
- Redis Docs  
  https://redis.io/docs/
- pgvector  
  https://github.com/pgvector/pgvector

### External Data Providers
- Polygon Stocks Overview  
  https://polygon.io/docs/rest/stocks/overview/
- Polygon Last Trade  
  https://polygon.io/docs/rest/stocks/trades-quotes/last-trade
- GNews Docs  
  https://docs.gnews.io/
- Deepgram Docs  
  https://developers.deepgram.com/documentation/
- Deepgram TTS  
  https://developers.deepgram.com/docs/text-to-speech
- Azure Speech TTS  
  https://learn.microsoft.com/en-us/azure/ai-services/Speech-Service/text-to-speech

## 관련 문서
- [[README]]
- [[Master_Index]]
- [[Feasibility]]
- [[System_Architecture]]
- [[Security_Model]]
- [[Tech_Stack_Decision]]

## 참고 자료
- 본 문서 자체가 참고 자료 색인이다.
> [!warning] Deprecated  
> Superseded by: [[Official_References]]
