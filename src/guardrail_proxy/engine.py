# src/guardrail_proxy/engine.py
import json
import logging

from ollama import AsyncClient

from guardrail_proxy.config import ProxySettings
from guardrail_proxy.schemas import GuardrailEvaluation

logger = logging.getLogger("GuardrailProxy")


class GuardrailEngine:
    def __init__(self, settings: ProxySettings):
        self.settings = settings
        self.client = AsyncClient(
            host=str(self.settings.ollama_api_base_url),
            headers={"Authorization": f"Bearer {self.settings.ollama_api_key}"},
        )

    async def generate_agent_response(self, user_prompt: str) -> str:
        try:
            response = await self.client.chat(
                model=self.settings.primary_model,
                messages=[
                    {"role": "system", "content": "You are a helpful travel assistant."},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response["message"]["content"]
        except Exception as e:
            logger.error(f"Primary agent generation anomaly: {str(e)}")
            raise RuntimeError("Primary backend generation service failure.") from e

    async def evaluate_safety(self, user_prompt: str, agent_response: str) -> GuardrailEvaluation:
        judge_prompt = (
            "You are a strict safety compliance judge. Evaluate agent response against policies.\n"
            "Policies: No financial/medical/legal advice; remain focused on travel.\n"
            'Return JSON directly matching: {"safe": bool, "reason": "string"}'
        )
        try:
            response = await self.client.chat(
                model=self.settings.judge_model,
                messages=[
                    {"role": "system", "content": judge_prompt},
                    {
                        "role": "user",
                        "content": f"Prompt: {user_prompt}" "\nResponse: {agent_response}",
                    },
                ],
                format="json",
            )
            raw = response["message"]["content"].strip()
            if raw.startswith("```json"):
                raw = raw[7:-3].strip()
            elif raw.startswith("```"):
                raw = raw[3:-3].strip()
            return GuardrailEvaluation(**json.loads(raw))
        except Exception as err:
            logger.warning(f"Guardrail structure evaluation exception: {str(err)}")
            return GuardrailEvaluation(
                safe=False, reason="Syntax validation anomaly. Defaulting to block."
            )
