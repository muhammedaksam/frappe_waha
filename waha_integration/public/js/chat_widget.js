$(document).ready(function () {
	if ($('#waha-chat-widget-root').length === 0) {
		$('body').append(`
			<div id="waha-chat-widget-root">
				<button class="waha-chat-toggle-btn" id="waha-chat-toggle" title="WhatsApp Chat">
					💬
				</button>

				<div class="waha-chat-drawer hidden" id="waha-chat-drawer">
					<div class="waha-chat-header">
						<span id="waha-chat-title">WhatsApp Desk</span>
						<button id="waha-chat-close" style="background:none;border:none;color:#fff;cursor:pointer;font-size:18px;">✕</button>
					</div>

					<div class="waha-chat-body" id="waha-chat-body">
						<div class="waha-contact-list" id="waha-contact-list"></div>
						<div class="waha-messages-container hidden" id="waha-messages-thread"></div>
					</div>

					<div class="waha-chat-footer hidden" id="waha-chat-footer">
						<button id="waha-back-to-contacts" style="border:none;background:none;cursor:pointer;font-size:16px;">⬅️</button>
						<input type="text" class="waha-chat-input" id="waha-chat-input" placeholder="Type a message..." />
						<button class="btn btn-sm btn-primary" id="waha-send-btn">Send</button>
					</div>
				</div>
			</div>
		`);

		let current_chat_id = null;

		$('#waha-chat-toggle').on('click', function () {
			$('#waha-chat-drawer').toggleClass('hidden');
			if (!$('#waha-chat-drawer').hasClass('hidden')) {
				load_contacts();
			}
		});

		$('#waha-chat-close').on('click', function () {
			$('#waha-chat-drawer').addClass('hidden');
		});

		$('#waha-back-to-contacts').on('click', function () {
			$('#waha-messages-thread').addClass('hidden');
			$('#waha-chat-footer').addClass('hidden');
			$('#waha-contact-list').removeClass('hidden');
			$('#waha-chat-title').text('WhatsApp Desk');
			current_chat_id = null;
			load_contacts();
		});

		function load_contacts() {
			frappe.call({
				method: 'waha_integration.api.chat.get_contacts',
				callback: function (r) {
					let contacts = r.message || [];
					let $list = $('#waha-contact-list').empty();

					if (contacts.length === 0) {
						$list.append('<div style="padding:16px;text-align:center;color:#666;">No recent WhatsApp chats</div>');
						return;
					}

					contacts.forEach(c => {
						let unread_badge = c.unread_count > 0 ? `<span class="badge badge-success" style="float:right;">${c.unread_count}</span>` : '';
						$list.append(`
							<div class="waha-contact-item" data-chat-id="${c.chat_id}" data-name="${c.full_name}">
								<div>
									<strong>${c.full_name}</strong>
									<br><small style="color:#777;">${c.phone_number}</small>
								</div>
								${unread_badge}
							</div>
						`);
					});

					$('.waha-contact-item').on('click', function () {
						current_chat_id = $(this).data('chat-id');
						let name = $(this).data('name');
						open_thread(current_chat_id, name);
					});
				}
			});
		}

		function open_thread(chat_id, name) {
			$('#waha-chat-title').text(name);
			$('#waha-contact-list').addClass('hidden');
			$('#waha-messages-thread').removeClass('hidden').empty();
			$('#waha-chat-footer').removeClass('hidden');

			frappe.call({
				method: 'waha_integration.api.chat.mark_read',
				args: { chat_id: chat_id }
			});

			frappe.call({
				method: 'waha_integration.api.chat.get_messages',
				args: { chat_id: chat_id },
				callback: function (r) {
					let msgs = r.message || [];
					let $thread = $('#waha-messages-thread');
					msgs.forEach(m => {
						let dir_class = m.direction === 'Outgoing' ? 'outgoing' : 'incoming';
						$thread.append(`
							<div class="waha-msg-bubble ${dir_class}">
								${m.content || ''}
							</div>
						`);
					});
					$thread.scrollTop($thread[0].scrollHeight);
				}
			});
		}

		$('#waha-send-btn').on('click', function () {
			let text = $('#waha-chat-input').val().trim();
			if (!text || !current_chat_id) return;

			$('#waha-chat-input').val('');
			$('#waha-messages-thread').append(`
				<div class="waha-msg-bubble outgoing">${text}</div>
			`);
			let $thread = $('#waha-messages-thread');
			$thread.scrollTop($thread[0].scrollHeight);

			frappe.call({
				method: 'waha_integration.api.chat.send_desk_message',
				args: { chat_id: current_chat_id, content: text }
			});
		});

		frappe.realtime.on('whatsapp_new_message', function (data) {
			if (current_chat_id && data.chat_id === current_chat_id) {
				$('#waha-messages-thread').append(`
					<div class="waha-msg-bubble incoming">${data.content}</div>
				`);
				let $thread = $('#waha-messages-thread');
				$thread.scrollTop($thread[0].scrollHeight);
			} else {
				frappe.show_alert({
					message: `New WhatsApp message from ${data.contact}: ${data.content}`,
					indicator: 'green'
				});
			}
		});
	}
});
