from typing import Optional
import re
import frappe
from frappe.model.document import Document

class WhatsAppKeywordReply(Document):
    enabled: Optional[int] = None
    keywords: Optional[str] = None
    match_type: Optional[str] = None
    response_type: Optional[str] = None
    reply_text: Optional[str] = None
    reply_media: Optional[str] = None
    python_script: Optional[str] = None

    def matches(self, incoming_text: str) -> bool:
        if not self.enabled or not incoming_text or not self.keywords:
            return False

        text = incoming_text.strip().lower()
        keyword_list = [k.strip().lower() for k in self.keywords.split(",") if k.strip()]

        if self.match_type == "Exact":
            return any(text == k for k in keyword_list)
        elif self.match_type == "Contains":
            return any(k in text for k in keyword_list)
        elif self.match_type == "StartsWith":
            return any(text.startswith(k) for k in keyword_list)
        elif self.match_type == "Regex":
            return any(re.search(k, incoming_text, re.IGNORECASE) for k in keyword_list)
        return False
