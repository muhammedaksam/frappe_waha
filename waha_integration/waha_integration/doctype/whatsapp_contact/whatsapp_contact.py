import frappe
from frappe.model.document import Document
from waha_integration.waha_client import format_chat_id

class WhatsAppContact(Document):
    def validate(self):
        if not self.chat_id and self.phone_number:
            self.chat_id = format_chat_id(self.phone_number)

        if not self.customer or not self.lead or not self.contact:
            self.auto_link_erpnext_entities()

    def auto_link_erpnext_entities(self):
        if not self.phone_number:
            return
        phone = "".join([c for c in self.phone_number if c.isdigit()])
        if not phone:
            return

        if not self.contact and frappe.db.exists("Contact", {"mobile_no": ["like", f"%{phone[-10:]}"]}):
            self.contact = frappe.db.get_value("Contact", {"mobile_no": ["like", f"%{phone[-10:]}"]})

        if not self.customer and frappe.db.exists("Customer", {"mobile_no": ["like", f"%{phone[-10:]}"]}):
            self.customer = frappe.db.get_value("Customer", {"mobile_no": ["like", f"%{phone[-10:]}"]})

        if not self.lead and frappe.db.exists("Lead", {"mobile_no": ["like", f"%{phone[-10:]}"]}):
            self.lead = frappe.db.get_value("Lead", {"mobile_no": ["like", f"%{phone[-10:]}"]})


@frappe.whitelist()
def get_or_create_contact(phone_number, name=None, account=None):
    chat_id = format_chat_id(phone_number)
    if frappe.db.exists("WhatsApp Contact", {"chat_id": chat_id}):
        return frappe.get_doc("WhatsApp Contact", {"chat_id": chat_id})

    doc = frappe.get_doc({
        "doctype": "WhatsApp Contact",
        "full_name": name or phone_number,
        "phone_number": phone_number,
        "chat_id": chat_id,
        "account": account
    })
    doc.insert(ignore_permissions=True)
    return doc
