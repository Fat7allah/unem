import frappe

@frappe.whitelist()
def get_member_details(member_id):
    """Get member details including membership status"""
    if not member_id:
        frappe.throw(_("Member ID is required"))
        
    member = frappe.get_doc("Member", member_id)
    membership = frappe.get_all(
        "Membership_Card",
        filters={"member": member_id},
        fields=["name", "membership_date", "expiry_date", "card_status"]
    )
    
    return {
        "member": member,
        "membership": membership[0] if membership else None
    }

@frappe.whitelist()
def get_structure_members(structure_type, position_type=None):
    """Get members by structure type and position"""
    filters = {"doctype": structure_type}
    if position_type:
        filters["position_type"] = position_type
        
    return frappe.get_all(
        structure_type,
        filters=filters,
        fields=["member", "position_type", "role"]
    )
