import json
from typing import Optional, Any
import frappe
from frappe.model.document import Document

class WhatsAppChatbotSession(Document):
    session_data_json: Optional[str] = None
    is_paused: Optional[int] = None
    pause_until: Optional[Any] = None

    def get_data(self) -> dict:
        if not self.session_data_json:
            return {}
        try:
            return json.loads(self.session_data_json)
        except Exception:
            return {}

    def set_data(self, data: dict):
        self.session_data_json = json.dumps(data, indent=2)

    def pause_session(self, minutes: int = 60):
        self.is_paused = 1
        self.pause_until = str(frappe.utils.add_to_date(frappe.utils.now_datetime(), minutes=minutes))
        self.save(ignore_permissions=True)

    def is_active(self) -> bool:
        if self.is_paused:
            if self.pause_until:
                dt = frappe.utils.get_datetime(self.pause_until)
                if dt and frappe.utils.now_datetime() < dt:
                    return False
            self.is_paused = 0
            self.save(ignore_permissions=True)
        return True
