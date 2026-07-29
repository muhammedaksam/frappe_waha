# Development & Bench Installation Guide

This document contains instructions for setting up and installing **WAHA Integration** (`waha_integration`) on a self-hosted Frappe bench instance or local development environment.

---

## 🚀 Manual Bench Installation

Navigate to your Frappe bench directory and run:

```bash
# 1. Get the app from GitHub
bench get-app https://github.com/muhammedaksam/frappe_waha

# 2. Install app on your site
bench --site [your-site-name] install-app waha_integration

# 3. Build Desk assets
bench build --app waha_integration
```

---

## 🛠️ Local Development & Testing

1. Ensure a local WAHA (WhatsApp HTTP API) server instance is running (e.g. `http://localhost:3000`).
2. Start the bench server:
   ```bash
   bench start
   ```
3. Run Python unit tests:
   ```bash
   bench --site [your-site-name] run-tests --app waha_integration
   ```
