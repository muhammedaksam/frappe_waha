frappe.ui.form.on('WhatsApp Account', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Start Session'), function() {
				frappe.call({
					method: 'start_session',
					doc: frm.doc,
					callback: function(r) {
						frappe.show_alert(__('Start command sent. Refreshing status...'));
						frm.reload_doc();
					}
				});
			}).addClass('btn-primary');

			frm.add_custom_button(__('Stop Session'), function() {
				frappe.call({
					method: 'stop_session',
					doc: frm.doc,
					callback: function(r) {
						frappe.show_alert(__('Stop command sent.'));
						frm.reload_doc();
					}
				});
			});

			frm.add_custom_button(__('Get QR Code'), function() {
				frappe.call({
					method: 'fetch_qr_code',
					doc: frm.doc,
					callback: function(r) {
						if (r.message && r.message.qr) {
							let qr = r.message.qr;
							let img_html = qr.startsWith('data:image') 
								? `<img src="${qr}" style="max-width:300px; margin:10px 0; border: 1px solid #ccc; padding: 10px;" />`
								: `<pre>${qr}</pre>`;
							frm.set_df_property('qr_code_html', 'options', img_html);
							frm.refresh_field('qr_code_html');
						} else {
							frappe.msgprint(__('No QR code returned or session already active.'));
						}
					}
				});
			});

			frm.add_custom_button(__('Sync Status'), function() {
				frappe.call({
					method: 'sync_status',
					doc: frm.doc,
					callback: function(r) {
						frappe.show_alert(__('Status updated: ' + (r.message ? r.message.status : '')));
						frm.reload_doc();
					}
				});
			});
		}
	}
});
