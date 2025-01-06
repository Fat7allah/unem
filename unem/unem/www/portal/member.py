import frappe
from frappe import _

def get_context(context):
    if not frappe.session.user or frappe.session.user == 'Guest':
        frappe.local.flags.redirect_location = '/login'
        raise frappe.Redirect
    
    context.pathname = '/portal/members'
    
    # Get member if editing
    member_name = frappe.form_dict.get('name')
    if member_name:
        if not frappe.has_permission('Member', 'write'):
            frappe.throw(_('Not permitted'), frappe.PermissionError)
        context.doc = frappe.get_doc('Member', member_name)
        
        # Get related membership cards
        context.membership_cards = frappe.get_all('Membership Card',
            filters={'member': member_name},
            fields=['name', 'issue_date', 'valid_until', 'status'],
            order_by='creation desc'
        )
    else:
        if not frappe.has_permission('Member', 'create'):
            frappe.throw(_('Not permitted'), frappe.PermissionError)
        context.doc = frappe._dict()

@frappe.whitelist()
def save_member():
    if not frappe.session.user or frappe.session.user == 'Guest':
        frappe.throw(_('Authentication required'), frappe.AuthenticationError)
    
    # Get form data
    data = frappe.form_dict
    
    try:
        if data.get('name'):
            # Update existing member
            if not frappe.has_permission('Member', 'write'):
                frappe.throw(_('Not permitted'), frappe.PermissionError)
            
            doc = frappe.get_doc('Member', data.get('name'))
            doc.update({
                'full_name': data.get('full_name'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'address': data.get('address'),
                'enabled': 1 if data.get('enabled') else 0
            })
            doc.save()
        else:
            # Create new member
            if not frappe.has_permission('Member', 'create'):
                frappe.throw(_('Not permitted'), frappe.PermissionError)
            
            doc = frappe.get_doc({
                'doctype': 'Member',
                'full_name': data.get('full_name'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'address': data.get('address'),
                'enabled': 1 if data.get('enabled') else 0
            })
            doc.insert()
        
        frappe.db.commit()
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/portal/members"
        
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response["type"] = "error"
        frappe.local.response["message"] = str(e)
