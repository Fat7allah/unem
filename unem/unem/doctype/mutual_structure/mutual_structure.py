# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Mutual_Structure(Document):
    def validate(self):
        self.validate_unique_position()
        self.validate_member_active()
        
    def validate_unique_position(self):
        """Ensure no duplicate positions in the same type"""
        if self.position_type and self.role:
            existing = frappe.db.exists("Mutual_Structure", {
                "position_type": self.position_type,
                "role": self.role,
                "name": ("!=", self.name)
            })
            if existing:
                frappe.throw("هذا المنصب مشغول بالفعل في هذا المكتب")
                
    def validate_member_active(self):
        """Ensure member has an active membership"""
        if self.member:
            active_card = frappe.db.exists("Membership_Card", {
                "member": self.member,
                "card_status": "المؤداة",
                "expiry_date": (">", frappe.utils.today())
            })
            if not active_card:
                frappe.throw("يجب أن يكون العضو لديه بطاقة عضوية سارية المفعول")
