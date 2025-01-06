import frappe

def execute():
    """Set website settings for UNEM app"""
    website_settings = frappe.get_doc("Website Settings")
    website_settings.home_page = "index"
    website_settings.save()
