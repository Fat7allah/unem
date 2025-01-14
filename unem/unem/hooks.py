from . import __version__ as app_version

app_name = "unem"
app_title = "UNEM"
app_publisher = "UNEM"
app_description = "UNEM"
app_email = "unem@example.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/unem/css/unem.css"
app_include_js = ["/assets/unem/js/workspace.js"]

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

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "index"

# website user home page (by Role)
role_home_page = {
    "Guest": "index",
    "System Manager": "index",
    "All": "index"
}

# Routing
website_route_rules = [
    {"from_route": "/", "to_route": "index"},
]

# Website Settings
website_context = {
    "home_page": "index"
}

# Installation
after_install = "unem.setup.landing_page.after_install"

# Boot Info
boot_session = "unem.startup.boot.boot_session"

# Override Website Settings
on_session_creation = "unem.startup.boot.on_session_creation"

# Website Redirects
website_redirects = [
    {"source": "/", "target": "/index"}
]

# Default website template
base_template = "templates/base.html"

# Website Context
website_context = {
    "base_template_path": "templates/base.html",
    "home_page": "index"
}

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#   "methods": "unem.utils.jinja_methods",
#   "filters": "unem.utils.jinja_filters"
# }

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
# ------------------
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
#   "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#   "Event": "frappe.desk.doctype.event.event.has_permission",
# }
