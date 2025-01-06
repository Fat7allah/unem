import frappe

def get_context(context):
    """Redirect root to index"""
    frappe.local.flags.redirect_location = '/index'
    raise frappe.Redirect
