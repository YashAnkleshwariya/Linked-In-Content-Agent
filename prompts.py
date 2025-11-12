# prompts.py

POST_BRIEF = (
    "You are a senior LinkedIn content strategist.\n"
    "Create a short, structured content brief for a LinkedIn post about:\n"
    "Topic: {topic}\n"
    "Audience: {audience}\n"
    "Tone: {tone}\n"
    "Please include Objective, Target audience summary, Tone, and 3 concise key points.\n"
    "Return plain text."
)

POST_DRAFT = (
    "You are a LinkedIn post writer.\n"
    "Use the brief below to write a compelling LinkedIn post.\n\n"
    "Brief:\n{brief}\n\n"
    "Guidelines:\n"
    "- Tone: {tone}\n"
    "- Audience: {audience}\n"
    "- Length: {length}\n"
    "- Hashtags: {hashtags}\n"
    "- End with this call to action: \"{call_to_action}\"\n\n"
    "Structure: Hook → Insight → CTA.\n"
    "Return only the post text."
)

POST_EDIT = (
    "You are a LinkedIn editor.\n"
    "Polish this draft for clarity, flow, and engagement.\n\n"
    "Draft:\n{draft}\n\n"
    "Return only the final, polished post."
)
