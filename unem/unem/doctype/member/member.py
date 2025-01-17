# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address

class Member(Document):
    def __init__(self, *args, **kwargs):
        super(Member, self).__init__(*args, **kwargs)
        self.flags.temp_province = None
        
    def validate(self):
        """
        Validate member data before saving.
        Ensures email, phone, and province data are valid.
        """
        frappe.msgprint(f"DEBUG - Validate: region={self.region}, province={self.province}")
        
        # Store the province value
        if self.province:
            self.flags.temp_province = self.province
            frappe.msgprint(f"DEBUG - Stored province in flags: {self.flags.temp_province}")
        
        self.validate_email()
        self.validate_phone()
        self.validate_province()
        self.set_title()
        
        # Double check province is still set
        frappe.msgprint(f"DEBUG - After Validation: region={self.region}, province={self.province}")
        
    def set_title(self):
        """Set title as First Name Last Name"""
        self.title = f"{self.first_name} {self.last_name}"
        
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
        frappe.msgprint(f"DEBUG - Validate Province: region={self.region}, province={self.province}")
        
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
        """
        frappe.msgprint(f"DEBUG - Before Save: region={self.region}, province={self.province}")
        
        # Ensure province is set from flags if available
        if not self.province and self.flags.temp_province:
            self.province = self.flags.temp_province
            
    def before_insert(self):
        """
        Handle data before first insert.
        """
        frappe.msgprint(f"DEBUG - Before Insert: region={self.region}, province={self.province}")
        
        # Ensure province is set from flags if available
        if not self.province and self.flags.temp_province:
            self.province = self.flags.temp_province
            
    def on_update(self):
        """
        Handle after save operations.
        """
        frappe.msgprint(f"DEBUG - On Update: region={self.region}, province={self.province}")
        
        # If province is missing but we have it in flags, set it directly
        if self.region and not self.province and self.flags.temp_province:
            frappe.msgprint(f"DEBUG - Setting province from flags: {self.flags.temp_province}")
            frappe.db.set_value("Member", self.name, "province", self.flags.temp_province, update_modified=False)
            frappe.db.commit()
            
    def after_insert(self):
        """
        Handle after insert operations.
        """
        frappe.msgprint(f"DEBUG - After Insert: region={self.region}, province={self.province}")
        
        # If province is missing but we have it in flags, set it directly
        if self.region and not self.province and self.flags.temp_province:
            frappe.msgprint(f"DEBUG - Setting province from flags: {self.flags.temp_province}")
            frappe.db.set_value("Member", self.name, "province", self.flags.temp_province, update_modified=False)
            frappe.db.commit()

    def load_from_db(self):
        """
        Override load_from_db to ensure province is loaded correctly
        """
        super(Member, self).load_from_db()
        
        # Only try to restore province if _doc_before_save exists
        if hasattr(self, '_doc_before_save') and self._doc_before_save:
            if 'province' in self._doc_before_save:
                self.province = self._doc_before_save['province']
            
    def as_dict(self, *args, **kwargs):
        """
        Override as_dict to ensure province is included in the document dictionary
        """
        d = super(Member, self).as_dict(*args, **kwargs)
        
        # Ensure province is included in the dictionary
        if hasattr(self, 'province'):
            d['province'] = self.province
            
        return d

    def autoname(self):
        """Set name as MEM-#### and title as First Name Last Name"""
        self.name = frappe.model.naming.make_autoname("MEM-.####")
        self.title = f"{self.first_name} {self.last_name}"

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
