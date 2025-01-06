import frappe

def get_context(context):
    if not frappe.session.user or frappe.session.user == 'Guest':
        frappe.local.flags.redirect_location = '/login'
        raise frappe.Redirect
    
    # Check permissions
    if not frappe.has_permission('Member', 'read'):
        frappe.throw(_('Not permitted'), frappe.PermissionError)
    
    context.pathname = '/portal/members'
    
    # Get members list
    context.members = frappe.get_list('Member',
        fields=['name', 'full_name', 'email', 'phone', 'enabled'],
        order_by='creation desc'
    )
