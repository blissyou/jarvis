# ADR: Hybrid Model Provider Strategy

Status: Accepted

## Context
JARVIS needs a model layer that does not depend on a single provider. LM Studio research indicates a strong fit for local stateful reasoning, while Ollama remains strong for fast stateless inference and OpenAI remains the fallback path.

Related:
- [[ADR_002_Model_Routing]]
- [[Model_Routing_Architecture]]
- [[Model_Router_Design]]

## Facts
- Fact: LM Studio supports OpenAI-compatible `/v1/responses`.
- Fact: LM Studio supports `previous_response_id`.
- Fact: Ollama is optimized for fast local inference.
- Fact: OpenAI offers a reliable remote fallback.

## Assumptions
- Assumption: LM Studio resource cost is acceptable when reserved for stateful reasoning tasks.
- Assumption: Splitting “reasoning” and “fast local inference” across providers is better than forcing one engine to do everything.

## Decision
Adopt a three-provider strategy:
- LM Studio as the primary local stateful reasoning engine
- Ollama as the fast stateless local engine
- OpenAI as fallback for local failure or higher-accuracy needs

## Consequences
Positive:
- avoids single-provider lock-in
- supports local stateful planning
- preserves low-latency simple-task handling
- keeps cloud usage optional

Negative:
- adds provider orchestration complexity
- introduces runtime session-state persistence
- requires logs that explain routing and fallback decisions

## Implementation Rule
- All model calls must go through `agent/model_router.py`
- No business logic may call LM Studio, Ollama, or OpenAI directly
