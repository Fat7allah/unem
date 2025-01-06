import frappe

def get_context(context):
    if not frappe.session.user or frappe.session.user == 'Guest':
        frappe.local.flags.redirect_location = '/login'
        raise frappe.Redirect

    # Get total income
    income_total = frappe.get_all(
        'Income Entry',
        filters={'docstatus': 1},
        fields=['sum(amount) as total']
    )
    context.total_income = income_total[0].total if income_total[0].total else 0

    # Get total expense
    expense_total = frappe.get_all(
        'Expense Entry',
        filters={'docstatus': 1},
        fields=['sum(amount) as total']
    )
    context.total_expense = expense_total[0].total if expense_total[0].total else 0

    # Get recent transactions
    income_transactions = frappe.get_all(
        'Income Entry',
        filters={'docstatus': 1},
        fields=['date', 'description', 'amount', '"Income" as type'],
        order_by='date desc',
        limit=5
    )

    expense_transactions = frappe.get_all(
        'Expense Entry',
        filters={'docstatus': 1},
        fields=['date', 'description', 'amount', '"Expense" as type'],
        order_by='date desc',
        limit=5
    )

    # Combine and sort transactions
    transactions = income_transactions + expense_transactions
    transactions.sort(key=lambda x: x.date, reverse=True)
    context.transactions = transactions[:5]

    context.currency = frappe.defaults.get_global_default('currency')
    context.show_sidebar = True
