import frappe

def get_home_page(user):
    """Get the home page for the user"""
    return "index"

def update_website_context(context):
    """Update website context to override default index"""
    context.home_page = "index"
    if frappe.local.request.path == "/":
        frappe.local.flags.redirect_location = "/index"
        raise frappe.Redirect
