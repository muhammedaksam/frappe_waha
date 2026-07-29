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
_trigger_notif = "waha_integration.waha_integration.doctype.whatsapp_notification.whatsapp_notification.trigger_notifications"

doc_events = {
	"Sales Invoice": {
		"after_insert": _trigger_notif,
		"on_update": _trigger_notif,
		"on_submit": _trigger_notif,
		"on_cancel": _trigger_notif,
		"on_trash": _trigger_notif,
	},
	"Sales Order": {
		"after_insert": _trigger_notif,
		"on_update": _trigger_notif,
		"on_submit": _trigger_notif,
		"on_cancel": _trigger_notif,
		"on_trash": _trigger_notif,
	},
	"Quotation": {
		"after_insert": _trigger_notif,
		"on_update": _trigger_notif,
		"on_submit": _trigger_notif,
		"on_cancel": _trigger_notif,
		"on_trash": _trigger_notif,
	},
	"Delivery Note": {
		"after_insert": _trigger_notif,
		"on_update": _trigger_notif,
		"on_submit": _trigger_notif,
		"on_cancel": _trigger_notif,
		"on_trash": _trigger_notif,
	},
	"Payment Entry": {
		"after_insert": _trigger_notif,
		"on_update": _trigger_notif,
		"on_submit": _trigger_notif,
		"on_cancel": _trigger_notif,
		"on_trash": _trigger_notif,
	},
	"Customer": {
		"after_insert": _trigger_notif,
		"on_update": _trigger_notif,
		"on_trash": _trigger_notif,
	},
	"Lead": {
		"after_insert": _trigger_notif,
		"on_update": _trigger_notif,
		"on_trash": _trigger_notif,
	},
	"Issue": {
		"after_insert": _trigger_notif,
		"on_update": _trigger_notif,
		"on_trash": _trigger_notif,
	},
	"Purchase Order": {
		"after_insert": _trigger_notif,
		"on_update": _trigger_notif,
		"on_submit": _trigger_notif,
		"on_cancel": _trigger_notif,
		"on_trash": _trigger_notif,
	},
}

# Scheduled Tasks
scheduler_events = {
	"hourly": [
		"waha_integration.waha_integration.doctype.whatsapp_account.whatsapp_account.sync_all_accounts"
	]
}
