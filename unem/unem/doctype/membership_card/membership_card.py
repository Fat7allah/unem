# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_years, getdate

class MembershipCard(Document):
    def validate(self):
        self.validate_dates()
        self.validate_card_number()
        
    def validate_dates(self):
        """Validate membership and expiry dates"""
        if self.membership_date and self.expiry_date:
            if getdate(self.expiry_date) <= getdate(self.membership_date):
                frappe.throw("تاريخ الانتهاء يجب أن يكون بعد تاريخ الإنخراط")
                
    def validate_card_number(self):
        """Generate unique card number if not provided"""
        if not self.card_number:
            # Get member details
            member = frappe.get_doc("Member", self.member)
            # Generate card number based on member details
            year = getdate().year
            province_code = self.get_province_code(member.province)
            sequence = frappe.db.count("Membership_Card") + 1
            self.card_number = f"{year}-{province_code}-{sequence:04d}"
            
    def get_province_code(self, province):
        """Get two-letter code for province"""
        province_codes = {
            "عمالة طنجة": "TN",
            "عمالة تطوان": "TT",
            "إقليم الفحص أنجرة": "FA"
        }
        return province_codes.get(province, "XX")
        
    def before_save(self):
        """Set expiry date to one year from membership date if not set"""
        if self.membership_date and not self.expiry_date:
            self.expiry_date = add_years(self.membership_date, 1)
