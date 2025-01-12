# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address

class Member(Document):
    def validate(self):
        """
        Validate member data before saving.
        Ensures email, phone, and province data are valid.
        """
        self.validate_email()
        self.validate_phone()
        self.validate_province()
        
    def validate_email(self):
        """
        Validate email format and uniqueness.
        Throws error if email is invalid or already exists.
        """
        if not self.email:
            return
            
        if not validate_email_address(self.email):
            frappe.throw("عنوان البريد الإلكتروني غير صالح")
        
        # Check email uniqueness
        if frappe.db.exists("Member", {
            "email": self.email,
            "name": ("!=", self.name)
        }):
            frappe.throw("البريد الإلكتروني مستخدم بالفعل")
                
    def validate_phone(self):
        """
        Validate phone number format.
        Removes non-digit characters and checks length.
        """
        if not self.phone:
            return
            
        # Remove non-digit characters
        self.phone = "".join(c for c in self.phone if c.isdigit())
        
        # Check phone length (8-15 digits)
        if not (8 <= len(self.phone) <= 15):
            frappe.throw("رقم الهاتف غير صالح")
                
    def validate_province(self):
        """
        Validate that selected province belongs to selected region.
        Throws error if province is missing or doesn't belong to region.
        """
        if not self.region:
            return
            
        if not self.province:
            frappe.throw("يجب تحديد الإقليم")
        
        # Ensure province exists
        if not frappe.db.exists("Province", self.province):
            frappe.throw("الإقليم غير موجود")
            
        # Get province document and validate region
        province_doc = frappe.get_doc("Province", self.province)
        if province_doc.region != self.region:
            frappe.throw(f"الإقليم المحدد لا ينتمي إلى {self.region}")
                
    def before_save(self):
        """
        Handle data changes before saving.
        Clears province when region changes.
        """
        if self.has_value_changed('region'):
            self.province = ''
            
@frappe.whitelist()
def get_provinces(doctype, txt, searchfield, start, page_len, filters=None):
    """
    Get filtered list of provinces based on region.
    
    Args:
        doctype: DocType being queried
        txt: Search text
        searchfield: Field to search in
        start: Start index for pagination
        page_len: Number of results per page
        filters: Additional filters (must include region)
    
    Returns:
        List of provinces matching search criteria
    """
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
