import json
import frappe
from typing import Optional, cast
from waha_integration.waha_integration.doctype.whatsapp_contact.whatsapp_contact import get_or_create_contact
from waha_integration.waha_integration.doctype.whatsapp_message.whatsapp_message import send_whatsapp_message
from waha_integration.waha_integration.doctype.whatsapp_chatbot_session.whatsapp_chatbot_session import WhatsAppChatbotSession
from waha_integration.waha_integration.doctype.whatsapp_keyword_reply.whatsapp_keyword_reply import WhatsAppKeywordReply
from waha_integration.waha_integration.doctype.whatsapp_ai_settings.whatsapp_ai_settings import WhatsAppAISettings

@frappe.whitelist(allow_guest=True)
def handle():
    """Webhook listener endpoint for WAHA server events."""
    if frappe.request.method != "POST":
        return {"status": "error", "message": "Only POST requests allowed"}

    data = frappe.request.get_json() or {}
    event_type = data.get("event")
    session_name = data.get("session", "default")
    payload = data.get("payload") or {}

    acc_name = frappe.db.get_value("WhatsApp Account", {"session_name": session_name, "enabled": 1})
    if not acc_name:
        acc_name = frappe.db.get_value("WhatsApp Account", {"is_default": 1, "enabled": 1})

    if acc_name and isinstance(acc_name, str):
        if event_type in ["message", "message.any"]:
            process_incoming_message(acc_name, payload)
        elif event_type in ["message.ack"]:
            process_message_ack(payload)
        elif event_type in ["session.status"]:
            process_session_status(session_name, payload)

    return {"status": "success"}


def process_incoming_message(account_name: str, payload: dict):
    if payload.get("fromMe"):
        return

    chat_id = payload.get("from") or payload.get("chatId")
    if not chat_id:
        return

    body = payload.get("body") or payload.get("text") or ""
    sender_phone = chat_id.split("@")[0] if "@" in chat_id else chat_id
    waha_id = payload.get("id")
    media_url = payload.get("mediaUrl") or (payload.get("hasMedia") and payload.get("media", {}).get("url"))
    msg_type = payload.get("_data", {}).get("type") or "text"

    contact_name = payload.get("_data", {}).get("notifyName") or sender_phone
    contact_doc = get_or_create_contact(sender_phone, name=contact_name, account=account_name)
    contact_doc.db_set("unread_count", (contact_doc.unread_count or 0) + 1)
    contact_doc.db_set("last_message_time", frappe.utils.now_datetime())

    msg = frappe.get_doc({
        "doctype": "WhatsApp Message",
        "account": account_name,
        "direction": "Incoming",
        "chat_id": chat_id,
        "sender": sender_phone,
        "message_type": msg_type if msg_type in ["text", "image", "video", "audio", "voice", "document"] else "text",
        "content": body,
        "media_url": media_url,
        "waha_message_id": waha_id,
        "status": "Received"
    })
    msg.insert(ignore_permissions=True)

    frappe.publish_realtime("whatsapp_new_message", {
        "chat_id": chat_id,
        "sender": sender_phone,
        "content": body,
        "contact": contact_doc.full_name,
        "name": msg.name
    })

    if msg.name:
        trigger_chatbot_engine(account_name, chat_id, body, msg.name)


def process_message_ack(payload: dict):
    waha_id = payload.get("id")
    ack_val = payload.get("ack")
    if not waha_id or not isinstance(ack_val, int):
        return

    status_map = {1: "Sent", 2: "Delivered", 3: "Read", 4: "Read"}
    new_status = status_map.get(ack_val)
    if new_status and frappe.db.exists("WhatsApp Message", {"waha_message_id": waha_id}):
        msg_name = frappe.db.get_value("WhatsApp Message", {"waha_message_id": waha_id})
        frappe.db.set_value("WhatsApp Message", msg_name, "status", new_status)


def process_session_status(session_name: str, payload: dict):
    status = payload.get("status")
    if status and frappe.db.exists("WhatsApp Account", {"session_name": session_name}):
        acc = frappe.db.get_value("WhatsApp Account", {"session_name": session_name})
        frappe.db.set_value("WhatsApp Account", acc, "status", status.upper())


def trigger_chatbot_engine(account_name: str, chat_id: str, message_text: str, message_name: str):
    """Processes active chatbot flows, keyword rules, and AI fallback."""
    if not message_text:
        return

    session_id = frappe.db.get_value("WhatsApp Chatbot Session", {"chat_id": chat_id})
    if session_id:
        session = cast(WhatsAppChatbotSession, frappe.get_doc("WhatsApp Chatbot Session", session_id))
        if not session.is_active():
            return

    rules = frappe.get_all("WhatsApp Keyword Reply", filters={"enabled": 1}, pluck="name")
    for r_name in rules:
        rule = frappe.get_doc("WhatsApp Keyword Reply", r_name)
        if hasattr(rule, "matches") and rule.matches(message_text):
            resp_type = getattr(rule, "response_type", None)
            reply_text = getattr(rule, "reply_text", None)
            reply_media = getattr(rule, "reply_media", None)
            script_code = getattr(rule, "python_script", None)

            if resp_type == "Text" and reply_text:
                send_whatsapp_message(account=account_name, chat_id=chat_id, text=reply_text)
                return
            elif resp_type == "Media" and reply_media:
                send_whatsapp_message(account=account_name, chat_id=chat_id, text=reply_text or "", media_url=reply_media)
                return
            elif resp_type == "Script" and script_code:
                try:
                    loc = {"chat_id": chat_id, "text": message_text, "account": account_name}
                    frappe.safe_eval(script_code, None, loc)
                except Exception as e:
                    frappe.log_error(f"Error executing keyword reply script {rule.name}: {e}")
                return

    ai_doc = frappe.get_single("WhatsApp AI Settings")
    if ai_doc and getattr(ai_doc, "enabled", 0):
        if hasattr(ai_doc, "generate_reply"):
            reply = ai_doc.generate_reply(message_text)
            if reply:
                send_whatsapp_message(account=account_name, chat_id=chat_id, text=reply)
