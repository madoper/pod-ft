__anchor__ = "llm-provider-router"
# schema-ref: project-schema.yaml#/shared_modules/0

from typing import Any, Protocol

from backend.shared.llm.contracts import LlmRequest, LlmResponse


class _PolicyEngine(Protocol):
    def select(self, task_type: str) -> list[str]: ...


class LlmProviderRouter:
    """All LLM calls go through this module. No direct calls from feature code."""

    def __init__(
        self, providers: dict[str, Any], policy_engine: _PolicyEngine | None = None
    ) -> None:
        self._providers = providers
        self._policy_engine = policy_engine

    async def invoke(self, request: LlmRequest) -> LlmResponse:
        candidates = (
            self._policy_engine.select(task_type=request.task_type)
            if self._policy_engine
            else list(self._providers)
        )
        last_error: Exception | None = None
        for provider_name in candidates:
            client = self._providers[provider_name]
            try:
                return await client.invoke(request)  # type: ignore[no-any-return]
            except Exception as exc:
                last_error = exc
                continue
        msg = f"All providers failed for task={request.task_type}: {last_error}"
        raise RuntimeError(msg)
