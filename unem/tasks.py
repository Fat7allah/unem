import frappe
from frappe.utils import today, add_days, getdate

def daily():
    """Daily scheduled tasks"""
    check_expiring_memberships()
    
def monthly():
    """Monthly scheduled tasks"""
    generate_monthly_reports()
    
def check_expiring_memberships():
    """Check and notify about memberships expiring in the next 30 days"""
    thirty_days_from_now = add_days(today(), 30)
    
    expiring_cards = frappe.get_all(
        "Membership_Card",
        filters={
            "expiry_date": ["between", [today(), thirty_days_from_now]],
            "card_status": "المؤداة"
        },
        fields=["name", "member", "expiry_date"]
    )
    
    for card in expiring_cards:
        member = frappe.get_doc("Member", card.member)
        if member.email:
            frappe.sendmail(
                recipients=[member.email],
                subject="تنبيه: بطاقة العضوية على وشك الانتهاء",
                message=f"بطاقة عضويتك ستنتهي في {card.expiry_date}. يرجى تجديد عضويتك."
            )
            
def generate_monthly_reports():
    """Generate monthly financial and membership reports"""
    # Financial summary
    income = frappe.get_all(
        "Income_Entry",
        filters={"date": ["this_month"]},
        fields=["sum(amount) as total_income"]
    )
    
    expenses = frappe.get_all(
        "Expense_Entry",
        filters={"date": ["this_month"]},
        fields=["sum(amount) as total_expenses"]
    )
    
    # Create monthly report
    report = frappe.get_doc({
        "doctype": "Monthly_Report",
        "month": getdate().strftime("%B %Y"),
        "total_income": income[0].total_income if income else 0,
        "total_expenses": expenses[0].total_expenses if expenses else 0
    })
    report.insert()
