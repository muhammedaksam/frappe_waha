$(document).on('app_ready', function () {
	frappe.router.on("change", () => {
		var route = frappe.get_route();
		if (route && route[0] == "Form") {
			let doctype = route[1];
			frappe.ui.form.on(doctype, {
				refresh: function (frm) {
					if (!frm.is_new()) {
						frm.page.add_menu_item(__("Send via WhatsApp"), function () {
							open_whatsapp_dialog(frm);
						});

						const transaction_doctypes = ["Sales Order", "Sales Invoice", "Quotation", "Delivery Note", "Payment Entry"];
						if (transaction_doctypes.includes(frm.doctype)) {
							frm.add_custom_button(__('WhatsApp PDF'), function () {
								send_transaction_whatsapp(frm);
							}, __('WhatsApp'));
						}
					}
				}
			});
		}
	});
});

function open_whatsapp_dialog(frm) {
	let recipient_phone = frm.doc.mobile_no || frm.doc.contact_mobile || frm.doc.phone || '';

	let d = new frappe.ui.Dialog({
		title: __('Send WhatsApp Message'),
		fields: [
			{
				label: __('Recipient Phone / Chat ID'),
				fieldname: 'recipient',
				fieldtype: 'Data',
				reqd: 1,
				default: recipient_phone
			},
			{
				label: __('WhatsApp Account'),
				fieldname: 'account',
				fieldtype: 'Link',
				options: 'WhatsApp Account',
				reqd: 1
			},
			{
				label: __('Template'),
				fieldname: 'template',
				fieldtype: 'Link',
				options: 'WhatsApp Template',
				onchange: function () {
					let t_name = d.get_value('template');
					if (t_name) {
						frappe.db.get_value('WhatsApp Template', t_name, 'body_text', (r) => {
							if (r && r.body_text) {
								d.set_value('message', r.body_text);
							}
						});
					}
				}
			},
			{
				label: __('Message Content'),
				fieldname: 'message',
				fieldtype: 'Text',
				reqd: 1
			}
		],
		primary_action_label: __('Send Message'),
		primary_action: function () {
			let vals = d.get_values();
			if (!vals) return;

			frappe.call({
				method: 'waha_integration.waha_integration.doctype.whatsapp_message.whatsapp_message.send_whatsapp_message',
				args: {
					account: vals.account,
					chat_id: vals.recipient,
					text: vals.message,
					reference_doctype: frm.doctype,
					reference_name: frm.docname
				},
				freeze: true,
				callback: function (r) {
					frappe.show_alert({ message: __('WhatsApp Message sent!'), indicator: 'green' });
					d.hide();
				}
			});
		}
	});
	d.show();
}

function send_transaction_whatsapp(frm) {
	let recipient_phone = frm.doc.mobile_no || frm.doc.contact_mobile || frm.doc.phone || '';

	frappe.prompt([
		{
			label: __('Recipient Phone Number'),
			fieldname: 'phone',
			fieldtype: 'Data',
			reqd: 1,
			default: recipient_phone
		},
		{
			label: __('WhatsApp Account'),
			fieldname: 'account',
			fieldtype: 'Link',
			options: 'WhatsApp Account',
			reqd: 1
		},
		{
			label: __('Message Note'),
			fieldname: 'note',
			fieldtype: 'Small Text',
			default: `Hello, please find attached PDF document for ${frm.doctype} ${frm.docname}. Thank you!`
		}
	], (values) => {
		frappe.call({
			method: 'frappe.client.get_value',
			args: {
				doctype: 'WhatsApp Account',
				filters: { name: values.account },
				fieldname: 'session_name'
			},
			callback: function (r) {
				frappe.show_alert({ message: __('Preparing document PDF & sending via WhatsApp...'), indicator: 'blue' });

				frappe.call({
					method: 'waha_integration.waha_integration.doctype.whatsapp_message.whatsapp_message.send_whatsapp_message',
					args: {
						account: values.account,
						chat_id: values.phone,
						text: values.note,
						reference_doctype: frm.doctype,
						reference_name: frm.docname
					},
					callback: function (res) {
						frappe.show_alert({ message: __('WhatsApp notification sent!'), indicator: 'green' });
					}
				});
			}
		});
	}, __('Send Document PDF via WhatsApp'), __('Send'));
}
