import frappe
from frappe import _

def get_context(context):
    if not frappe.session.user or frappe.session.user == 'Guest':
        frappe.local.flags.redirect_location = '/login'
        raise frappe.Redirect

    context.pathname = '/'
    
    # Member stats
    context.member_count = frappe.db.count('Member', {'enabled': 1})
    context.active_cards = frappe.db.count('Membership Card', {'status': 'Active'})
    
    # Organization stats
    context.unem_units = frappe.db.count('UNEM_Structure')
    context.mutual_units = frappe.db.count('Mutual_Structure')
    
    # Financial stats
    income_total = frappe.get_all(
        'Income Entry',
        filters={'docstatus': 1},
        fields=['sum(amount) as total']
    )
    context.total_income = income_total[0].total if income_total[0].total else 0

    expense_total = frappe.get_all(
        'Expense Entry',
        filters={'docstatus': 1},
        fields=['sum(amount) as total']
    )
    context.total_expense = expense_total[0].total if expense_total[0].total else 0
    
    context.currency = frappe.defaults.get_global_default('currency')
    
    # Recent activities
    activities = frappe.get_all(
        'Activity Log',
        filters={
            'reference_doctype': ['in', ['Member', 'Membership Card', 'UNEM_Structure', 
                                       'Mutual_Structure', 'Income Entry', 'Expense Entry']]
        },
        fields=['reference_doctype', 'description', 'owner', 'creation'],
        order_by='creation desc',
        limit=10
    )
    
    # Add indicator colors based on doctype
    for activity in activities:
        if activity.reference_doctype in ['Member', 'Membership Card']:
            activity.indicator_color = 'blue'
        elif activity.reference_doctype in ['UNEM_Structure', 'Mutual_Structure']:
            activity.indicator_color = 'orange'
        elif activity.reference_doctype == 'Income Entry':
            activity.indicator_color = 'green'
        else:
            activity.indicator_color = 'red'
    
    context.activities = activities
