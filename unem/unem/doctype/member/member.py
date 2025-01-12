# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Member(Document):
    def validate(self):
        self.validate_email()
        self.validate_phone()
        self.validate_province()
        
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
                
    def validate_province(self):
        """Validate that the selected province belongs to the selected region"""
        if self.region:
            if not self.province:
                frappe.throw("يجب تحديد الإقليم")
            
            # Ensure province exists
            if not frappe.db.exists("Province", self.province):
                frappe.throw("الإقليم غير موجود")
                
            # Get province document
            province_doc = frappe.get_doc("Province", self.province)
            if province_doc.region != self.region:
                frappe.throw(f"الإقليم المحدد لا ينتمي إلى {self.region}")
                
    def before_save(self):
        """Handle province before saving"""
        if self.has_value_changed('region'):
            self.province = ''

@frappe.whitelist()
def get_provinces(doctype, txt, searchfield, start, page_len, filters=None):
    """Get provinces based on selected region"""
    if isinstance(filters, str):
        import json
        filters = json.loads(filters)
        
    region = filters.get('region') if isinstance(filters, dict) else None
    if not region:
        return []
        
    # Get provinces from database
    provinces = frappe.get_all('Province',
        filters={'region': region},
        or_filters={
            'name': ['like', f'%{txt}%'],
            'province_name': ['like', f'%{txt}%']
        },
        fields=['name', 'province_name'],
        start=int(start),
        page_length=int(page_len),
        order_by='province_name asc'
    )
    
    return [[p.name, p.province_name] for p in provinces]
