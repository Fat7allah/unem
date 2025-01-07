# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class AcademicYear(Document):
    def validate(self):
        self.validate_dates()
        self.validate_active_year()
        
    def validate_dates(self):
        """Validate start and end dates"""
        if self.start_date and self.end_date:
            if getdate(self.start_date) > getdate(self.end_date):
                frappe.throw("تاريخ البداية يجب أن يكون قبل تاريخ النهاية")
                
    def validate_active_year(self):
        """Ensure only one academic year is active at a time"""
        if self.is_active:
            active_year = frappe.db.exists("Academic Year", {
                "is_active": 1,
                "name": ("!=", self.name)
            })
            if active_year:
                frappe.throw("هناك سنة دراسية نشطة بالفعل. يرجى إلغاء تنشيط السنة الحالية أولاً.")
