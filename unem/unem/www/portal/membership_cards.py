import frappe

def get_context(context):
    if not frappe.session.user or frappe.session.user == 'Guest':
        frappe.local.flags.redirect_location = '/login'
        raise frappe.Redirect
    
    # Check permissions
    if not frappe.has_permission('Membership Card', 'read'):
        frappe.throw(_('Not permitted'), frappe.PermissionError)
    
    context.pathname = '/portal/membership-cards'
    
    # Get membership cards list
    context.cards = frappe.get_list('Membership Card',
        fields=['name', 'member', 'member_name', 'issue_date', 'expiry_date', 'status'],
        order_by='creation desc'
    )
