import frappe
from frappe.model.document import Document

class Member(Document):
    def validate(self):
        """
        Validate member data before saving
        """
        self.validate_email()
        self.validate_phone()
        
    def validate_email(self):
        """
        Validate email format and uniqueness
        """
        if self.email:
            if not frappe.utils.validate_email_address(self.email):
                frappe.throw("عنوان البريد الإلكتروني غير صالح")
            
            # Check email uniqueness
            if frappe.db.exists("Member", {
                "email": self.email,
                "name": ("!=", self.name)
            }):
                frappe.throw("البريد الإلكتروني مستخدم بالفعل")
                
    def validate_phone(self):
        """
        Validate phone number format
        """
        if self.phone:
            # Remove spaces and dashes
            self.phone = "".join(c for c in self.phone if c.isdigit())
            
            if not (8 <= len(self.phone) <= 15):
                frappe.throw("رقم الهاتف غير صالح")

def after_member_insert(doc, method):
    """
    After member creation hook
    """
    # Create default membership card
    create_membership_card(doc)
    
def on_member_update(doc, method):
    """
    On member update hook
    """
    # Update related documents
    update_related_documents(doc)
    
def create_membership_card(member):
    """
    Create a new membership card for the member
    """
    if not frappe.db.exists("Membership_Card", {"member": member.name}):
        card = frappe.get_doc({
            "doctype": "Membership_Card",
            "member": member.name,
            "membership_date": frappe.utils.today(),
            "expiry_date": frappe.utils.add_years(None, 1),
            "card_status": "غير المؤداة"
        })
        card.insert(ignore_permissions=True)
        
def update_related_documents(member):
    """
    Update related documents when member information changes
    """
    # Update membership cards
    cards = frappe.get_all("Membership_Card", 
        filters={"member": member.name},
        fields=["name"])
    
    for card in cards:
        frappe.db.set_value("Membership_Card", card.name, {
            "member_name": member.name
        })
