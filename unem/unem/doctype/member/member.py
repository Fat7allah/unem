# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Member(Document):
    def validate(self):
        self.validate_email()
        self.validate_phone()
        
    def validate_email(self):
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
        if self.phone:
            # Remove spaces and dashes
            self.phone = "".join(c for c in self.phone if c.isdigit())
            
            if not (8 <= len(self.phone) <= 15):
                frappe.throw("رقم الهاتف غير صالح")
                
    def after_insert(self):
        """Create default membership card after member creation"""
        self.create_membership_card()
        
    def create_membership_card(self):
        """Create a new membership card"""
        if not frappe.db.exists("Membership_Card", {"member": self.name}):
            card = frappe.get_doc({
                "doctype": "Membership_Card",
                "member": self.name,
                "membership_date": frappe.utils.today(),
                "expiry_date": frappe.utils.add_years(None, 1),
                "card_status": "غير المؤداة"
            })
            card.insert(ignore_permissions=True)
