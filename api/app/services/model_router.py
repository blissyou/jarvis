from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class ModelRoute:
    provider: str
    route_reason: str
    estimated_cost_krw: float
    model: str | None = None


@dataclass
class ModelReply:
    route: ModelRoute
    text: str


@dataclass
class ProviderHealth:
    name: str
    available: bool
    base_url: str | None
    model: str | None
    detail: str


class LocalProvider:
    name = "local_echo"

    def available(self) -> bool:
        return True

    def health(self) -> ProviderHealth:
        return ProviderHealth(
            name=self.name,
            available=True,
            base_url=None,
            model=None,
            detail="Always available fallback provider.",
        )

    def infer(self, text: str) -> str:
        return (
            "요청을 이해했습니다. 현재는 로컬 모델 공급자가 연결되지 않아 fallback 응답을 사용했습니다. "
            "JARVIS는 OpenClaw 런타임 위의 Voice Layer로 동작하며, 도구 실행은 승인 정책을 따릅니다."
        )


class OllamaProvider:
    name = "ollama"

    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        self.fast_model = os.getenv("OLLAMA_FAST_MODEL", os.getenv("OLLAMA_MODEL", "llama3.2"))
        self.korean_fast_model = os.getenv("OLLAMA_KOREAN_FAST_MODEL", "qwen2.5:1.5b")
        self.reasoning_model = os.getenv("OLLAMA_REASONING_MODEL", os.getenv("OLLAMA_MODEL", "qwen3:8b"))
        self.model = os.getenv("OLLAMA_MODEL", self.fast_model)
        self.timeout = float(os.getenv("JARVIS_MODEL_TIMEOUT_SECONDS", "1.5"))

    def model_for(self, reasoning: bool, korean: bool = False) -> str:
        if korean and not reasoning:
            return self.korean_fast_model
        return self.reasoning_model if reasoning else self.fast_model

    def _model_is_available(self, configured_model: str, available_models: list[str | None]) -> bool:
        candidates = {configured_model, f"{configured_model}:latest"}
        return any(model in candidates for model in available_models)

    def health(self) -> ProviderHealth:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                data = response.json()
            available_models = [model.get("name") for model in data.get("models", []) if isinstance(model, dict)]
            configured_models = [self.fast_model, self.korean_fast_model, self.reasoning_model]
            missing = [model for model in configured_models if not self._model_is_available(model, available_models)]
            detail = "Ollama API is reachable."
            if missing:
                detail = f"Ollama API is reachable, but missing configured model(s): {', '.join(missing)}."
            return ProviderHealth(
                self.name,
                True,
                self.base_url,
                f"fast={self.fast_model}; korean_fast={self.korean_fast_model}; reasoning={self.reasoning_model}",
                detail,
            )
        except Exception as exc:  # noqa: BLE001 - health should never crash API
            return ProviderHealth(
                self.name,
                False,
                self.base_url,
                f"fast={self.fast_model}; korean_fast={self.korean_fast_model}; reasoning={self.reasoning_model}",
                str(exc),
            )

    def available(self) -> bool:
        return self.health().available

    def infer(self, text: str, reasoning: bool = False, korean: bool = False) -> str:
        model = self.model_for(reasoning, korean=korean)
        system_prompt = (
            "You are JARVIS, a concise voice-first assistant running as a product layer on OpenClaw. "
            "OpenClaw owns execution, sessions, tools, approvals, and background tasks. "
            "JARVIS owns STT/TTS, transcript UX, and the HUD. Mention approval gates when relevant, "
            "and never offer payments, transfers, orders, or financial trade execution."
        )
        if korean:
            if not reasoning and model == self.korean_fast_model:
                system_prompt = "자비스처럼 자연스러운 한국어로 한두 문장만 답하세요. Markdown, 이모지, 내부 추론은 금지입니다."
            else:
                system_prompt = (
                    "당신은 로컬 데스크톱 비서 JARVIS입니다. 반드시 자연스러운 한국어로만 답하세요. "
                    "중국어, 영어, 태국어, 일본어를 섞지 마세요. 지금 실제로 가능한 기능만 말하세요. "
                    "현재 가능한 기능은 짧은 대화, 마이크 입력, 음성 출력, transcript 표시, 세션 상태 확인, "
                    "OpenClaw 기반 승인형 도구 실행 준비, 개발용 채팅 UI입니다. 아직 실제 음악 재생, 화면 제어, 일정 관리, 파일 이동은 완성 기능처럼 말하지 마세요. "
                    "결제, 송금, 주문, 매매 같은 금융 거래 실행은 MVP 범위 밖이라고 말하세요. "
                    "음성 출력에 적합하게 이모지, 특수기호, 목록 장식을 쓰지 마세요. "
                    "Markdown 문법을 쓰지 마세요. 별표, 백틱, 하이픈 목록, 번호 목록, 굵게 표시 문법을 출력하지 마세요. "
                    "내부 추론 과정을 출력하지 말고 바로 최종 답변만 말하세요."
                )
            if model.startswith("qwen3"):
                system_prompt = f"/no_think\n{system_prompt}"
        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": text},
            ],
            "stream": False,
            "think": False,
            "keep_alive": os.getenv("OLLAMA_KEEP_ALIVE", "30m"),
            "options": {"temperature": 0.1, "top_p": 0.75, "repeat_penalty": 1.1, "num_predict": 48 if not reasoning and korean else 90},
        }
        with httpx.Client(timeout=max(self.timeout, 30.0)) as client:
            response = client.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
        return str(data.get("message", {}).get("content") or data.get("response") or "")

    def warmup(self) -> None:
        payload: dict[str, Any] = {
            "model": self.korean_fast_model,
            "prompt": "준비",
            "stream": False,
            "keep_alive": os.getenv("OLLAMA_KEEP_ALIVE", "30m"),
            "options": {"num_predict": 1},
        }
        try:
            with httpx.Client(timeout=20.0) as client:
                client.post(f"{self.base_url}/api/generate", json=payload)
        except Exception:
            return


class LMStudioProvider:
    name = "lmstudio"

    def __init__(self) -> None:
        self.base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234").rstrip("/")
        self.model = os.getenv("LMSTUDIO_MODEL", "local-model")
        self.timeout = float(os.getenv("JARVIS_MODEL_TIMEOUT_SECONDS", "1.5"))

    def health(self) -> ProviderHealth:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/v1/models")
                response.raise_for_status()
                data = response.json()
            models = data.get("data", []) if isinstance(data, dict) else []
            detail = f"LM Studio compatible API reachable. {len(models)} model(s) reported."
            return ProviderHealth(self.name, True, self.base_url, self.model, detail)
        except Exception as exc:  # noqa: BLE001
            return ProviderHealth(self.name, False, self.base_url, self.model, str(exc))

    def available(self) -> bool:
        return self.health().available

    def infer(self, text: str, korean: bool = False) -> str:
        system_prompt = "You are JARVIS, a concise voice-first assistant layered on OpenClaw. Prefer safe plans, mention approval when actions are risky, and never offer financial transaction execution."
        if korean:
            system_prompt = (
                "당신은 OpenClaw 위에서 동작하는 voice-first 비서 JARVIS입니다. 반드시 자연스러운 한국어로만 짧게 답하세요. "
                "JARVIS는 STT/TTS와 HUD를 담당하고 OpenClaw는 실행, 승인, 세션, 도구를 담당합니다. "
                "결제, 송금, 주문, 매매 같은 금융 거래 실행은 MVP 범위 밖입니다. 현재 구현된 기능과 미구현 기능을 구분해서 말하세요. Markdown 문법이나 목록 장식을 쓰지 마세요."
            )
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            "temperature": 0.1,
            "stream": False,
        }
        with httpx.Client(timeout=max(self.timeout, 20.0)) as client:
            response = client.post(f"{self.base_url}/v1/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
        return str(data.get("choices", [{}])[0].get("message", {}).get("content") or "")


class ModelRouter:
    def __init__(self) -> None:
        self.ollama = OllamaProvider()
        self.lmstudio = LMStudioProvider()
        self.echo = LocalProvider()

    def health(self) -> list[ProviderHealth]:
        return [self.ollama.health(), self.lmstudio.health(), self.echo.health()]

    def warmup(self) -> None:
        self.ollama.warmup()

    def _provider_by_name(self, name: str) -> OllamaProvider | LMStudioProvider | LocalProvider:
        if name == "ollama":
            return self.ollama
        if name in {"lmstudio", "ai_studio"}:
            return self.lmstudio
        return self.echo

    def _is_complex(self, text: str) -> bool:
        lowered = text.lower()
        return any(word in lowered for word in ["plan", "analyze", "debug", "explain", "설계", "분석", "디버그"])

    def _contains_korean(self, text: str) -> bool:
        return any("\uac00" <= char <= "\ud7a3" for char in text)

    def _clean_for_voice(self, text: str, korean: bool) -> str:
        if not korean:
            return text
        cleaned = re.sub(r"[\U0001f300-\U0001faff\u2600-\u27bf]", "", text)
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()

    def _instant_reply(self, text: str) -> str | None:
        normalized = re.sub(r"\s+", " ", text.strip().lower())
        if not normalized or not self._contains_korean(normalized):
            return None

        if any(word in normalized for word in ["들려", "내 말", "내말", "마이크"]):
            return "네, 들립니다. 바로 대화할 수 있어요."
        if any(word in normalized for word in ["뭘 할", "무엇을 할", "기능", "할 수 있어"]):
            return "지금은 짧은 대화, 마이크 입력, 음성 출력, transcript 표시, OpenClaw 기반 승인형 도구 실행 준비를 할 수 있어요. 금융 거래 실행은 MVP 범위 밖입니다."
        if any(word in normalized for word in ["준비", "상태", "켜졌", "실행"]):
            return "준비됐습니다. 마이크나 채팅으로 명령해 주세요."
        if any(word in normalized for word in ["짧게", "간단히", "빨리"]) and any(word in normalized for word in ["대답", "답", "말"]):
            return "네, 짧고 빠르게 답하겠습니다."
        if any(word in normalized for word in ["고마워", "수고", "좋아"]):
            return "좋습니다. 다음 명령을 기다릴게요."

        return None

    def _ordered_provider_names(self, text: str, sensitive: bool) -> list[str]:
        mode = os.getenv("JARVIS_PROVIDER_MODE", "local_dual")
        fast = os.getenv("JARVIS_FAST_PROVIDER", "ollama")
        reasoning = os.getenv("JARVIS_REASONING_PROVIDER", "ollama")

        if mode == "ollama_only":
            return ["ollama", "local_echo"]
        if mode in {"lmstudio_only", "ai_studio_only"}:
            return ["lmstudio", "local_echo"]
        if sensitive or self._is_complex(text):
            return [reasoning, fast, "local_echo"]
        return [fast, reasoning, "local_echo"]

    def choose_route(self, text: str, sensitive: bool = False, cloud_allowed: bool = False) -> ModelRoute:
        wants_reasoning = sensitive or self._is_complex(text)
        wants_korean = self._contains_korean(text)
        for provider_name in self._ordered_provider_names(text, sensitive):
            provider = self._provider_by_name(provider_name)
            if provider.available():
                reason = "local dual routing"
                model: str | None = None
                if provider.name == "lmstudio":
                    reason = "local reasoning provider for complex or sensitive planning"
                    model = provider.model
                elif provider.name == "ollama":
                    model = provider.model_for(wants_reasoning, korean=wants_korean)
                    if wants_korean:
                        reason = "fast Korean model for short voice turns" if not wants_reasoning else "Korean reasoning model for complex planning"
                    else:
                        reason = "local reasoning model for complex or sensitive planning" if wants_reasoning else "fast local model for short turns"
                elif provider.name == "local_echo":
                    reason = "fallback provider because configured local APIs were unavailable"
                return ModelRoute(provider=provider.name, route_reason=reason, estimated_cost_krw=0.0, model=model)
        return ModelRoute(provider="local_echo", route_reason="fallback provider", estimated_cost_krw=0.0)

    def infer(self, text: str, sensitive: bool = False, cloud_allowed: bool = False) -> ModelReply:
        instant = None if sensitive or self._is_complex(text) else self._instant_reply(text)
        if instant:
            return ModelReply(
                route=ModelRoute(
                    provider="local_intent",
                    route_reason="instant Korean voice intent matched; skipped LLM latency",
                    estimated_cost_krw=0.0,
                    model=None,
                ),
                text=instant,
            )

        route = self.choose_route(text, sensitive=sensitive, cloud_allowed=cloud_allowed)
        provider = self._provider_by_name(route.provider)
        korean = self._contains_korean(text)
        try:
            if isinstance(provider, OllamaProvider):
                reply = provider.infer(text, reasoning=sensitive or self._is_complex(text), korean=korean)
            elif isinstance(provider, LMStudioProvider):
                reply = provider.infer(text, korean=korean)
            else:
                reply = provider.infer(text)
        except Exception as exc:  # noqa: BLE001
            fallback_route = ModelRoute(
                provider="local_echo",
                route_reason=f"{route.provider} inference failed; fallback used: {exc}",
                estimated_cost_krw=0.0,
            )
            return ModelReply(route=fallback_route, text=self.echo.infer(text))
        return ModelReply(route=route, text=self._clean_for_voice(reply or self.echo.infer(text), korean=korean))


router = ModelRouter()
