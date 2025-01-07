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

@frappe.whitelist()
def get_active_members(doctype, txt, searchfield, start, page_len, filters):
    """Get members with active membership cards"""
    return frappe.db.sql("""
        SELECT DISTINCT m.name, m.full_name_ar
        FROM `tabMember` m
        INNER JOIN `tabMembership_Card` mc ON mc.member = m.name
        WHERE mc.card_status = 'المؤداة'
        AND mc.expiry_date > CURDATE()
        AND (m.name LIKE %(txt)s OR m.full_name_ar LIKE %(txt)s)
        ORDER BY m.full_name_ar
        LIMIT %(start)s, %(page_len)s
    """, {
        'txt': f"%{txt}%",
        'start': start,
        'page_len': page_len
    })
