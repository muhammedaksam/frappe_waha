from typing import Optional
import frappe
from waha_integration.waha_integration.doctype.whatsapp_message.whatsapp_message import send_whatsapp_message

@frappe.whitelist()
def get_contacts():
    """Fetch contacts list for Frappe Desk chat drawer."""
    return frappe.get_all(
        "WhatsApp Contact",
        fields=["name", "full_name", "phone_number", "chat_id", "unread_count", "last_message_time", "assigned_user", "customer", "lead"],
        order_by="last_message_time desc",
        limit=50
    )

@frappe.whitelist()
def get_messages(chat_id: str, limit: int = 50):
    """Fetch conversation history for a given chat_id."""
    return frappe.get_all(
        "WhatsApp Message",
        filters={"chat_id": chat_id},
        fields=["name", "direction", "content", "media_url", "message_type", "status", "creation"],
        order_by="creation asc",
        limit=limit
    )

@frappe.whitelist()
def send_desk_message(chat_id: str, content: str, account: Optional[str] = None, media_url: Optional[str] = None):
    """Send message from Desk chat interface."""
    if not account:
        account = frappe.db.get_value("WhatsApp Account", {"is_default": 1, "enabled": 1}) or frappe.db.get_value("WhatsApp Account", {"enabled": 1})
    if not account:
        frappe.throw("No active WhatsApp Account found")

    return send_whatsapp_message(
        account=account,
        chat_id=chat_id,
        text=content,
        media_url=media_url
    )

@frappe.whitelist()
def mark_read(chat_id: str):
    """Reset unread message count for contact."""
    if frappe.db.exists("WhatsApp Contact", {"chat_id": chat_id}):
        c_name = frappe.db.get_value("WhatsApp Contact", {"chat_id": chat_id})
        frappe.db.set_value("WhatsApp Contact", c_name, "unread_count", 0)
    return {"status": "ok"}
