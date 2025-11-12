# crew.py
from typing import Dict
from agents import strategist_agent, writer_agent, editor_agent
from prompts import POST_BRIEF, POST_DRAFT, POST_EDIT
import json


class LinkedInContentCrew:
    def __init__(self, topic, audience, tone, length, hashtags, call_to_action, temperature=0.7):
        self.topic = topic
        self.audience = audience
        self.tone = tone
        self.length = length
        self.hashtags = hashtags
        self.call_to_action = call_to_action
        self.temperature = temperature

    def _safe_generate(self, agent, prompt, stage):
        try:
            result = agent.generate(prompt, temperature=self.temperature)
            return result.strip()
        except Exception as e:
            return f"(❌ Error during {stage}: {e})"

    def kickoff(self) -> Dict[str, str]:
        brief_prompt = POST_BRIEF.format(topic=self.topic, audience=self.audience, tone=self.tone)
        brief_text = self._safe_generate(strategist_agent, brief_prompt, "brief")

        draft_prompt = POST_DRAFT.format(
            brief=brief_text,
            tone=self.tone,
            audience=self.audience,
            length=self.length,
            hashtags=self.hashtags,
            call_to_action=self.call_to_action,
        )
        draft_text = self._safe_generate(writer_agent, draft_prompt, "draft")

        edit_prompt = POST_EDIT.format(draft=draft_text)
        final_post = self._safe_generate(editor_agent, edit_prompt, "edit")

        out = {"brief": brief_text, "draft": draft_text, "final_post": final_post}
        try:
            json.dumps(out)
        except Exception:
            out = {k: str(v) for k, v in out.items()}
        return out
