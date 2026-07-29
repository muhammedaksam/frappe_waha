import frappe
from frappe.model.document import Document
from waha_integration.waha_integration.doctype.whatsapp_message.whatsapp_message import send_whatsapp_message

class WhatsAppNotification(Document):
    def evaluate_condition(self, doc) -> bool:
        if not self.condition:
            return True
        try:
            return bool(frappe.safe_eval(self.condition, None, {"doc": doc}))
        except Exception as e:
            frappe.log_error(f"Error evaluating WhatsApp Notification condition for {self.name}: {e}")
            return False

    def get_recipient_phone(self, doc) -> str:
        if self.static_phone:
            return self.static_phone
        if self.recipient_field:
            val = doc.get(self.recipient_field)
            if val:
                return str(val)
        if doc.get("contact_mobile"):
            return str(doc.get("contact_mobile"))
        if doc.get("mobile_no"):
            return str(doc.get("mobile_no"))
        return ""

    def process(self, doc):
        if not self.enabled:
            return
        if not self.evaluate_condition(doc):
            return

        recipient = self.get_recipient_phone(doc)
        if not recipient:
            return

        rendered_message = frappe.render_template(  # nosemgrep: frappe-semgrep-rules.rules.security.frappe-ssti
            self.message_body, {"doc": doc}
        )

        pdf_url = None
        if self.attach_pdf:
            try:
                pdf_bytes = frappe.get_print(doc.doctype, doc.name, self.print_format, as_pdf=True)
                filename = f"{doc.doctype}_{doc.name}.pdf"
                _file = frappe.get_doc({
                    "doctype": "File",
                    "file_name": filename,
                    "content": pdf_bytes,
                    "is_private": 0
                })
                _file.save(ignore_permissions=True)
                pdf_url = _file.file_url
            except Exception as e:
                frappe.log_error(f"Error generating PDF attachment for {doc.doctype} {doc.name}: {e}")

        res = send_whatsapp_message(
            account=self.account,
            chat_id=recipient,
            text=rendered_message,
            message_type="document" if pdf_url else "text",
            media_url=pdf_url,
            reference_doctype=doc.doctype,
            reference_name=doc.name
        )

        if self.set_field_after_send and hasattr(doc, self.set_field_after_send):
            doc.db_set(self.set_field_after_send, self.set_value_after_send or 1)

        return res


def trigger_notifications(doc, method):
    """Global doc event hook triggered on all DocTypes."""
    if not frappe.db.table_exists("WhatsApp Notification"):
        return

    event = method
    notifications = frappe.get_all("WhatsApp Notification", filters={
        "document_type": doc.doctype,
        "event": event,
        "enabled": 1
    }, pluck="name")

    for notif_name in notifications:
        notif = frappe.get_doc("WhatsApp Notification", notif_name)
        notif.process(doc)
