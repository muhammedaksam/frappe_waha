app_name = "waha_integration"
app_title = "WAHA Integration"
app_publisher = "Muhammed Mustafa AKŞAM"
app_description = "WhatsApp Integration for Frappe & ERPNext using WAHA"
app_email = "info@muhammedaksam.com.tr"
app_license = "mit"

# Send non-GET requests for this app's endpoints as native `application/json`
# bodies instead of form-encoded, per-key JSON-stringified values.
use_json_request_body = True

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "waha_integration",
# 		"logo": "/assets/waha_integration/logo.png",
# 		"title": "WAHA Integration",
# 		"route": "/waha_integration",
# 		"has_permission": "waha_integration.api.permission.has_app_permission",
# 	}
# ]

# Companion apps that extend a host app (instead of taking their own apps-screen icon) can pin
# their workspaces into the host app's workspace dock (rail) with this hook. Declaring it keeps
# the app off the apps screen, so it takes precedence over any add_to_apps_screen above. Who can
# see a pinned workspace is controlled by that workspace's own Roles table.
# add_to_workspace_dock = [
# 	{
# 		"app": "erpnext",
# 		"workspace": "My Workspace",
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/waha_integration/css/waha_integration.css"
# app_include_js = "/assets/waha_integration/js/waha_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/waha_integration/css/waha_integration.css"
# web_include_js = "/assets/waha_integration/js/waha_integration.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "waha_integration/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "waha_integration/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "waha_integration.utils.jinja_methods",
# 	"filters": "waha_integration.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "waha_integration.install.before_install"
# after_install = "waha_integration.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "waha_integration.uninstall.before_uninstall"
# after_uninstall = "waha_integration.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "waha_integration.utils.before_app_install"
# after_app_install = "waha_integration.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "waha_integration.utils.before_app_uninstall"
# after_app_uninstall = "waha_integration.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "waha_integration.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "waha_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"waha_integration.tasks.all"
# 	],
# 	"daily": [
# 		"waha_integration.tasks.daily"
# 	],
# 	"hourly": [
# 		"waha_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"waha_integration.tasks.weekly"
# 	],
# 	"monthly": [
# 		"waha_integration.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "waha_integration.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "waha_integration.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "waha_integration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "waha_integration.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["waha_integration.utils.before_request"]
# after_request = ["waha_integration.utils.after_request"]

# Job Events
# ----------
# before_job = ["waha_integration.utils.before_job"]
# after_job = ["waha_integration.utils.after_job"]

# after_file_upload = ["waha_integration.utils.after_file_upload"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"waha_integration.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# Require all whitelisted methods to have type annotations
require_type_annotated_api_methods = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

