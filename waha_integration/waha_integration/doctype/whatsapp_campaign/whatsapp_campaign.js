frappe.ui.form.on('WhatsApp Campaign', {
	refresh: function(frm) {
		if (frm.doc.status === 'Draft' || frm.doc.status === 'Scheduled') {
			frm.add_custom_button(__('Start Campaign'), function() {
				frappe.call({
					method: 'start_campaign',
					doc: frm.doc,
					callback: function(r) {
						frappe.show_alert(__('Campaign enqueued for processing.'));
						frm.reload_doc();
					}
				});
			}).addClass('btn-primary');
		}
	}
});
