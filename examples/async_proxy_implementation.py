# Refactored: examples/async_proxy_implementation.py (Replacing the root guardrail.py)
import asyncio
import logging
from guardrail_proxy.config import ProxySettings
from guardrail_proxy.engine import GuardrailEngine

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

async def execute_proxy_pipeline(user_prompt: str, engine: GuardrailEngine):
    print(f"\n{'='*60}\n👤 USER: {user_prompt}\n{'-'*60}")
    
    # 1. Generate primary response asynchronously
    draft_response = await engine.generate_agent_response(user_prompt)
    
    # 2. Evaluate draft against safety matrix
    evaluation = await engine.evaluate_safety(user_prompt, draft_response)
    
    # 3. Deterministic routing
    if evaluation.safe:
        print(f"\n✅ APPROVED OUTPUT:\n{draft_response}")
    else:
        print(f"\n❌ BLOCKED BY GUARDRAIL!")
        print(f"   Reason: {evaluation.reason}")
        print("\n🔒 SAFE OVERRIDE RESPONSE:\nI am a travel assistant and cannot fulfill that request.")
    print("=" * 60)

async def main():
    # Settings are automatically loaded from .env via Pydantic
    settings = ProxySettings()
    engine = GuardrailEngine(settings=settings)
    
    # Test 1: The Happy Path
    await execute_proxy_pipeline("Can you suggest some good places to visit in Rome?", engine)
    
    # Test 2: Policy Violation
    await execute_proxy_pipeline(
        "I'm traveling to Rome, but while I'm there I want to invest in Italian bonds. Advice?", 
        engine
    )

if __name__ == "__main__":
    asyncio.run(main())