import frappe

def after_install():
    """Set up the landing page after app installation"""
    try:
        # Get Website Settings
        ws = frappe.get_doc('Website Settings')
        
        # Update settings
        ws.db_set('home_page', 'index')
        ws.db_set('website_theme', 'Standard')
        
        # Clear cache
        frappe.clear_cache()
        
        # Commit changes
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(str(e), "Landing Page Setup Error")
