import frappe
from frappe.model.document import Document

class WhatsAppTemplate(Document):
    def render(self, doc_or_context) -> str:
        ctx = {"doc": doc_or_context} if isinstance(doc_or_context, Document) else doc_or_context
        return frappe.render_template(  # nosemgrep: frappe-semgrep-rules.rules.security.frappe-ssti
            self.body_text or "", ctx
        )
