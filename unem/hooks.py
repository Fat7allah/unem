app_name = "unem"
app_title = "UNEM"
app_publisher = "UNEM"
app_description = "Union Nationale de l'Enseignement au Maroc Management System"
app_email = "admin@unem.ma"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/unem/css/unem.css"
# app_include_js = "/assets/unem/js/unem.js"

# include js, css files in header of web template
# web_include_css = "/assets/unem/css/unem.css"
# web_include_js = "/assets/unem/js/unem.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "unem/public/scss/website"

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

# DocTypes to be included
doctype_js = {
    "Member": "public/js/member.js",
    "Membership_Card": "public/js/membership_card.js",
    "UNEM_Structure": "public/js/unem_structure.js",
    "Mutual_Structure": "public/js/mutual_structure.js",
    "Income_Entry": "public/js/income_entry.js",
    "Expense_Entry": "public/js/expense_entry.js"
}

# Custom Scripts
doctype_list_js = {
    "Member": "public/js/member_list.js",
    "Membership_Card": "public/js/membership_card_list.js",
    "Income_Entry": "public/js/income_entry_list.js",
    "Expense_Entry": "public/js/expense_entry_list.js"
}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "unem.utils.jinja_methods",
#	"filters": "unem.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "unem.install.before_install"
# after_install = "unem.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "unem.uninstall.before_uninstall"
# after_uninstall = "unem.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "unem.utils.before_app_install"
# after_app_install = "unem.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "unem.utils.before_app_uninstall"
# after_app_uninstall = "unem.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "unem.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"unem.tasks.all"
#	],
#	"daily": [
#		"unem.tasks.daily"
#	],
#	"hourly": [
#		"unem.tasks.hourly"
#	],
#	"weekly": [
#		"unem.tasks.weekly"
#	],
#	"monthly": [
#		"unem.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "unem.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "unem.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "unem.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["unem.utils.before_request"]
# after_request = ["unem.utils.after_request"]

# Job Events
# ----------
# before_job = ["unem.utils.before_job"]
# after_job = ["unem.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"unem.auth.validate"
# ]

# Translation
# ----------------
translation_fields = ["title", "label", "description", "content"]
translated_search_fields = ["title", "label", "description", "content"]

# Translations
# -----------
# Add translations for your app. Example:
translations = [
    {
        "source_text": "Member Management",
        "translated_text": "إدارة الأعضاء",
        "language_code": "ar"
    },
    {
        "source_text": "Financial Management",
        "translated_text": "الإدارة المالية",
        "language_code": "ar"
    }
]

# Fixtures
fixtures = [
    {
        "doctype": "Region",
        "filters": [["name", "like", "%"]]
    },
    {
        "doctype": "Province",
        "filters": [["name", "like", "%"]]
    },
    {
        "doctype": "Profession",
        "filters": [["name", "like", "%"]]
    },
    {
        "doctype": "Teaching Specialty",
        "filters": [["name", "like", "%"]]
    }
]
