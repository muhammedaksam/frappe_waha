import frappe
from frappe.model.document import Document
from waha_integration.waha_client import WahaService

class WhatsAppMessage(Document):
    def send_now(self):
        if self.direction != "Outgoing":
            return
        if not self.account:
            frappe.throw("WhatsApp Account is required to send message")

        acc = frappe.get_doc("WhatsApp Account", self.account)
        service = acc.get_service()

        try:
            res = None
            if self.message_type == "text" or not self.media_url:
                res = service.send_text(
                    session_name=acc.session_name,
                    chat_id=self.chat_id,
                    text=self.content or ""
                )
            else:
                res = service.send_file(
                    session_name=acc.session_name,
                    chat_id=self.chat_id,
                    file_url=self.media_url,
                    caption=self.content
                )

            if isinstance(res, dict) and "error" in res:
                self.db_set("status", "Failed")
                self.db_set("error_message", str(res["error"]))
            else:
                self.db_set("status", "Sent")
                msg_id = res.get("id") if isinstance(res, dict) else None
                if msg_id:
                    self.db_set("waha_message_id", str(msg_id))
            return res
        finally:
            service.close()

    def on_submit(self):
        self.send_now()


@frappe.whitelist()
def send_whatsapp_message(account, chat_id, text, message_type="text", media_url=None, reference_doctype=None, reference_name=None):
    """Utility method to quickly send a WhatsApp message."""
    doc = frappe.get_doc({
        "doctype": "WhatsApp Message",
        "account": account,
        "direction": "Outgoing",
        "chat_id": chat_id,
        "message_type": message_type,
        "content": text,
        "media_url": media_url,
        "reference_doctype": reference_doctype,
        "reference_name": reference_name,
        "status": "Pending"
    })
    doc.insert(ignore_permissions=True)
    res = doc.send_now()
    return {"message_id": doc.name, "response": res}
