import frappe
from frappe.model.document import Document
from waha_integration.waha_integration.doctype.whatsapp_message.whatsapp_message import send_whatsapp_message

class WhatsAppCampaign(Document):
    def validate(self):
        self.total_recipients = len(self.recipients)

    @frappe.whitelist()
    def start_campaign(self):
        if not self.recipients:
            frappe.throw("No recipients added to campaign")

        self.db_set("status", "Processing")
        frappe.enqueue(
            "waha_integration.waha_integration.doctype.whatsapp_campaign.whatsapp_campaign.process_campaign_job",
            campaign_name=self.name,
            queue="long"
        )
        return {"status": "enqueued"}


def process_campaign_job(campaign_name: str):
    doc = frappe.get_doc("WhatsApp Campaign", campaign_name)
    sent = 0
    failed = 0

    for r in doc.recipients:
        if r.status == "Sent":
            sent += 1
            continue

        res = send_whatsapp_message(
            account=doc.account,
            chat_id=r.phone_number,
            text=doc.message_body,
            reference_doctype="WhatsApp Campaign",
            reference_name=doc.name
        )

        if res and isinstance(res.get("response"), dict) and "error" in res.get("response"):
            r.db_set("status", "Failed")
            r.db_set("error_message", str(res["response"]["error"]))
            failed += 1
        else:
            r.db_set("status", "Sent")
            sent += 1

    doc.db_set("sent_count", sent)
    doc.db_set("failed_count", failed)
    doc.db_set("status", "Completed" if (sent + failed) >= len(doc.recipients) else "Processing")
