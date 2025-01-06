import frappe

def get_context(context):
    """Add data to the context for the home page"""
    context.stats = get_quick_stats()
    return context

def get_quick_stats():
    """Get quick statistics for the dashboard"""
    stats = {
        'total_members': get_total_members(),
        'active_cards': get_active_cards(),
        'total_income': format_currency(get_total_income()),
        'total_expense': format_currency(get_total_expense())
    }
    return stats

def get_total_members():
    """Get total number of members"""
    return frappe.db.count('UNEM Member')

def get_active_cards():
    """Get number of active membership cards"""
    return frappe.db.count('Membership Card', {'status': 'Active'})

def get_total_income():
    """Get total income amount"""
    result = frappe.db.sql("""
        SELECT IFNULL(SUM(amount), 0) as total
        FROM `tabIncome Entry`
        WHERE docstatus = 1
    """)
    return result[0][0] if result else 0

def get_total_expense():
    """Get total expense amount"""
    result = frappe.db.sql("""
        SELECT IFNULL(SUM(amount), 0) as total
        FROM `tabExpense Entry`
        WHERE docstatus = 1
    """)
    return result[0][0] if result else 0

def format_currency(amount):
    """Format amount as currency"""
    return frappe.format_value(amount, {'fieldtype': 'Currency'})
