import frappe
from frappe.model.document import Document
from frappe.render_template import render_template

class WhatsAppTemplate(Document):
    def render(self, doc_or_context) -> str:
        ctx = {"doc": doc_or_context} if isinstance(doc_or_context, Document) else doc_or_context
        return render_template(self.body_text or "", ctx)
