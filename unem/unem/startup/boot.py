import frappe

def boot_session(bootinfo):
    """Update boot session info"""
    bootinfo.home_page = "index"

def on_session_creation():
    """Set the landing page on session creation"""
    if not frappe.db.exists("Website Settings"):
        return
        
    website_settings = frappe.get_doc("Website Settings")
    website_settings.home_page = "index"
    website_settings.save()
