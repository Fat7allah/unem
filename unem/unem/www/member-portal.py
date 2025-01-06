import frappe

def get_context(context):
    if not frappe.session.user or frappe.session.user == 'Guest':
        frappe.local.flags.redirect_location = '/login'
        raise frappe.Redirect

    context.doc = frappe.get_doc('Member', {'user': frappe.session.user})
    
    # Get recent activities
    activities = frappe.get_all(
        'Activity Log',
        filters={
            'user': frappe.session.user,
            'reference_doctype': 'Member'
        },
        fields=['description', 'creation'],
        order_by='creation desc',
        limit=5
    )
    
    context.activities = activities
    context.show_sidebar = True
