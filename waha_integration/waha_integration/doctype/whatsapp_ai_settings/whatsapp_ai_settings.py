from typing import Optional
import frappe
from frappe.model.document import Document

class WhatsAppAISettings(Document):
    enabled: Optional[int] = None
    enable_rag: Optional[int] = None
    system_prompt: Optional[str] = None
    provider: Optional[str] = None
    model_name: Optional[str] = None

    def generate_reply(self, user_prompt: str) -> str:
        if not self.enabled:
            return ""

        api_key = self.get_password("api_key")
        if not api_key:
            return "AI service API key is missing."

        context_str = ""
        if self.enable_rag and frappe.db.table_exists("Item"):
            items = frappe.get_all("Item", fields=["item_code", "item_name", "standard_rate", "description"], limit=10)
            if items:
                context_str = "\nAvailable Products:\n" + "\n".join([
                    f"- {i.get('item_name')} ({i.get('item_code')}): {i.get('standard_rate')} currency. {i.get('description') or ''}"
                    for i in items
                ])

        full_prompt = f"{self.system_prompt}\n{context_str}\n\nUser Question: {user_prompt}"

        try:
            if self.provider == "OpenAI":
                import requests
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": self.model_name or "gpt-4o-mini",
                    "messages": [{"role": "user", "content": full_prompt}],
                    "max_tokens": 500
                }
                r = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=15)
                if r.status_code == 200:
                    return r.json()["choices"][0]["message"]["content"].strip()
                return f"AI Error: {r.text}"
            else:
                return "AI provider not implemented or configured."
        except Exception as e:
            frappe.log_error(f"Error generating AI response: {e}")
            return "Sorry, I am unable to process your request at the moment."
