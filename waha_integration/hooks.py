app_name = "waha_integration"
app_title = "WAHA Integration"
app_publisher = "Muhammed Mustafa AKŞAM"
app_description = "WhatsApp Integration for Frappe & ERPNext using WAHA"
app_email = "info@muhammedaksam.com.tr"
app_license = "mit"

use_json_request_body = True

# Includes in <head>
app_include_js = [
	"/assets/waha_integration/js/waha_integration.js",
	"/assets/waha_integration/js/chat_widget.js"
]

app_include_css = [
	"/assets/waha_integration/css/chat_widget.css"
]

# Document Events
doc_events = {
	"*": {
		"after_insert": "waha_integration.waha_integration.doctype.whatsapp_notification.whatsapp_notification.trigger_notifications",
		"on_update": "waha_integration.waha_integration.doctype.whatsapp_notification.whatsapp_notification.trigger_notifications",
		"on_submit": "waha_integration.waha_integration.doctype.whatsapp_notification.whatsapp_notification.trigger_notifications",
		"on_cancel": "waha_integration.waha_integration.doctype.whatsapp_notification.whatsapp_notification.trigger_notifications",
		"on_trash": "waha_integration.waha_integration.doctype.whatsapp_notification.whatsapp_notification.trigger_notifications"
	}
}

# Scheduled Tasks
scheduler_events = {
	"hourly": [
		"waha_integration.waha_integration.doctype.whatsapp_account.whatsapp_account.sync_all_accounts"
	]
}
