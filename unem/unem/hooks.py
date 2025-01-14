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
app_include_js = ["/assets/unem/js/workspace.js", "/assets/unem/js/breadcrumb_fix.js"]

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
doctype_js = {
    "Member": "client_scripts/member/member.js",
    "Membership_Card": "client_scripts/membership_card/membership_card.js",
    "Membership_Card_Management": "client_scripts/membership_card_management/membership_card_management.js",
    "UNEM_Structure": "client_scripts/unem_structure/unem_structure.js",
    "Mutual_Structure": "client_scripts/mutual_structure/mutual_structure.js",
    "Region": "client_scripts/region/region.js",
    "Province": "client_scripts/province/province.js"
}

# Extend website
extends_website = True

extend_website_page = {
    "Workspace": {
        "Member": "member-management",
        "Membership_Card": "member-management",
        "Membership_Card_Management": "member-management",
        "UNEM_Structure": "member-management",
        "Mutual_Structure": "member-management",
        "Region": "member-management",
        "Province": "member-management"
    }
}

# Override doctype list js
doctype_list_js = {
    "Member": "public/js/member_list.js",
    "Membership_Card": "public/js/membership_card_list.js",
    "Membership_Card_Management": "public/js/membership_card_management_list.js",
    "UNEM_Structure": "public/js/unem_structure_list.js",
    "Mutual_Structure": "public/js/mutual_structure_list.js",
    "Region": "public/js/region_list.js",
    "Province": "public/js/province_list.js"
}

# Module configurations
module_doctypes = {
    "member-management": [
        "Member",
        "Membership_Card",
        "Membership_Card_Management",
        "UNEM_Structure",
        "Mutual_Structure",
        "Region",
        "Province"
    ]
}

# Workspace configurations
workspace_doctypes = {
    "member-management": [
        "Member",
        "Membership_Card",
        "Membership_Card_Management",
        "UNEM_Structure",
        "Mutual_Structure",
        "Region",
        "Province"
    ]
}

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
