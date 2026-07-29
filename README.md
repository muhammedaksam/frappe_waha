# Frappe WAHA (WhatsApp Integration for Frappe & ERPNext)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Frappe Framework](https://img.shields.io/badge/Frappe-v14%20%7C%20v15-blue.svg)](https://frappeframework.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)

A feature-complete, modern WhatsApp integration app for **Frappe Framework** and **ERPNext**, powered by **WAHA (WhatsApp HTTP API)** and `waha-py`.

---

## ✨ Features

- 📱 **Multi-Account & Live QR Code Setup**: Connect multiple WhatsApp accounts using WAHA HTTP API with live QR code rendering inside Frappe Desk.
- 💬 **Two-Way Messaging & Rich Media**: Full support for text, images, videos, audio, voice notes, documents, location, interactive buttons, and list messages.
- ⚡ **Dynamic DocType Notification Triggers**: Trigger automated WhatsApp messages on document events (`after_insert`, `on_update`, `on_submit`, `on_cancel`, `on_trash`) or schedulers (`Hourly`, `Daily`) with Jinja/Python conditions, PDF document attachments, and post-send field updates.
- 📢 **Bulk Campaigns & Messaging**: Filter target recipients from any DocType (Customer, Lead, Contact, etc.), schedule mass campaigns, and track real-time delivery progress.
- 🤖 **Automated Chatbot & AI Fallback**:
  - **Keyword Rules**: Exact, Contains, StartsWith, and Regex matching for Text, Media, Python Script, or Flow replies.
  - **Multi-Step Flow Builder**: Interactive question flows with user input collection and automatic ERPNext document creation.
  - **Human Agent Handoff**: Pause bot logic per contact during active agent conversations.
  - **AI Integration**: Intelligent fallback using OpenAI, Anthropic Claude, or Google Gemini with ERPNext product catalog grounding.
- 💬 **Frappe Desk Real-Time Chat UI Widget**: Floating Desk chat drawer powered by Socket.IO real-time events, contact assignment, unread counters, and sound alerts.
- 📄 **ERPNext Transaction Integration**: Quick "Send via WhatsApp" form menu action and one-click "WhatsApp PDF" buttons for Sales Orders, Invoices, Quotations, Delivery Notes, and Payment Entries.

---

## ⚙️ Overview & Setup

### 1. Configure WhatsApp Account

1. Open **WhatsApp Account** in Frappe Desk.
2. Enter your **WAHA Server URL** (e.g. `http://localhost:3000`), **API Key**, and **WAHA Session Name**.
3. Click **Start Session** and then **Get QR Code** to scan and authenticate your WhatsApp account.

### 2. Configure Dynamic Notifications

1. Go to **WhatsApp Notification**.
2. Select target **DocType** (e.g. `Sales Invoice`) and **Trigger Event** (`on_submit`).
3. Set your Jinja template message body and check **Attach Document PDF**.

### 3. Real-time Desk Chat UI

Click the floating WhatsApp chat bubble in Frappe Desk to open the live conversation drawer.

### 4. Self-Hosted & Development Setup

For manual CLI installation commands see [DEVELOPMENT.md](DEVELOPMENT.md).

---

## 🛠️ Tech Stack & SDK

- **SDK**: Built with [waha-py](https://github.com/muhammedaksam/waha-py) (WhatsApp HTTP API SDK).
- **Framework**: Frappe Framework (v14 / v15) & ERPNext.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

**Author**: [Muhammed Mustafa AKŞAM](https://github.com/muhammedaksam)
