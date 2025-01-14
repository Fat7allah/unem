import frappe

def get_context(context):
    # Override workspace for member management doctypes
    member_management_doctypes = [
        "Member",
        "Membership_Card",
        "Membership_Card_Management",
        "UNEM_Structure",
        "Mutual_Structure",
        "Region",
        "Province"
    ]
    
    doctype = frappe.form_dict.get("doctype")
    if doctype in member_management_doctypes:
        context.workspace = "member-management"
