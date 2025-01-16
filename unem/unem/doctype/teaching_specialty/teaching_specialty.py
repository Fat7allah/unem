# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TeachingSpecialty(Document):
    def validate(self):
        """
        Ensure teaching specialty is only linked to teaching professions
        """
        teaching_professions = ['التدريس الابتدائي', 'التدريس الإعدادي', 'التدريس التأهيلي']
        if self.profession not in teaching_professions:
            frappe.throw("يمكن إضافة التخصص فقط للمهن التعليمية")
