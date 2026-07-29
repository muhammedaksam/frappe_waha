import frappe
from frappe.model.document import Document
from waha_integration.waha_client import WahaService

class WhatsAppAccount(Document):
    def get_service(self) -> WahaService:
        api_key = self.get_password("api_key") if self.api_key else None
        return WahaService(base_url=self.server_url, api_key=api_key)

    @frappe.whitelist()
    def start_session(self):
        service = self.get_service()
        try:
            res = service.start_session(self.session_name)
            self.db_set("status", "STARTING")
            return res
        finally:
            service.close()

    @frappe.whitelist()
    def stop_session(self):
        service = self.get_service()
        try:
            res = service.stop_session(self.session_name)
            self.db_set("status", "STOPPED")
            return res
        finally:
            service.close()

    @frappe.whitelist()
    def fetch_qr_code(self):
        service = self.get_service()
        try:
            qr = service.get_qr_code(self.session_name)
            return {"qr": qr}
        finally:
            service.close()

    @frappe.whitelist()
    def sync_status(self):
        service = self.get_service()
        try:
            sessions = service.list_sessions()
            for s in sessions:
                if isinstance(s, dict) and s.get("name") == self.session_name:
                    status = s.get("status", "STOPPED").upper()
                    self.db_set("status", status)
                    return {"status": status}
            return {"status": self.status}
        finally:
            service.close()


def sync_all_accounts():
    if not frappe.db.table_exists("WhatsApp Account"):
        return
    accounts = frappe.get_all("WhatsApp Account", filters={"enabled": 1}, pluck="name")
    for acc_name in accounts:
        try:
            doc = frappe.get_doc("WhatsApp Account", acc_name)
            doc.sync_status()
        except Exception as e:
            frappe.log_error(f"Error syncing status for WhatsApp account {acc_name}: {e}")
