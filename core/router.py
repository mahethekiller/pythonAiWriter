"""
Centralized LLM Task Router & Cost Audit Logger for PythonAiWriter.
Routes tasks based on cost vs quality requirements and records agent run metrics.
"""

import time
from typing import Tuple, Dict, Any, Optional
from core.llm_client import MultiProviderLLMClient, calculate_cost_usd
from core.db import DatabaseManager


class LLMRouter:
    """Task Router that dispatches requests to optimal providers/models and logs run metrics."""

    def __init__(
        self, 
        active_provider: str = "OpenAI", 
        active_model: str = "gpt-4o-mini", 
        api_key: str = "", 
        base_url: Optional[str] = None,
        db_mgr: Optional[DatabaseManager] = None
    ):
        self.active_provider = active_provider
        self.active_model = active_model
        self.api_key = api_key
        self.base_url = base_url
        self.db = db_mgr or DatabaseManager()

    def call_task(
        self, 
        task_type: str, 
        system_prompt: str, 
        user_prompt: str, 
        override_provider: Optional[str] = None, 
        override_model: Optional[str] = None
    ) -> Tuple[str, int, int, int]:
        """Dispatches an LLM task, records execution latency, tokens, cost, and logs to SQLite database."""
        provider = override_provider or self.active_provider
        model = override_model or self.active_model

        client = MultiProviderLLMClient(
            provider=provider,
            api_key=self.api_key,
            model=model,
            base_url=self.base_url
        )

        start_t = time.time()
        content, p_tokens, c_tokens, t_tokens = client.generate_text(system_prompt, user_prompt)
        latency = round(time.time() - start_t, 2)
        cost_usd = calculate_cost_usd(model, p_tokens, c_tokens)

        # Log agent run to SQLite database for budget audit
        try:
            self.db.log_agent_run(
                task_type=task_type,
                provider=provider,
                model=model,
                prompt_tokens=p_tokens,
                completion_tokens=c_tokens,
                cost_usd=cost_usd,
                latency_sec=latency
            )
        except Exception:
            pass

        return content, p_tokens, c_tokens, t_tokens

    def completion(
        self, 
        task_type: str, 
        prompt: str, 
        temperature: float = 0.7, 
        system_prompt: str = "You are an expert search engine assistant."
    ) -> Tuple[str, Dict[str, Any]]:
        """Convenience method returning (content, metrics_dict)."""
        content, p_tokens, c_tokens, t_tokens = self.call_task(task_type, system_prompt, prompt)
        cost_usd = calculate_cost_usd(self.active_model, p_tokens, c_tokens)
        metrics = {
            "prompt_tokens": p_tokens,
            "completion_tokens": c_tokens,
            "total_tokens": t_tokens,
            "cost_usd": cost_usd
        }
        return content, metrics
