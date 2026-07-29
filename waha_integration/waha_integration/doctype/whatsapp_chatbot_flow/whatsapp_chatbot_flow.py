import frappe
from frappe.model.document import Document

class WhatsAppChatbotFlow(Document):
    def get_step(self, index: int):
        if 0 <= index < len(self.steps):
            return self.steps[index]
        return None
