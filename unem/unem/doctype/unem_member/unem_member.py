# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address

class UNEMMember(Document):
    def __init__(self, *args, **kwargs):
        super(UNEMMember, self).__init__(*args, **kwargs)
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
        
        # Double check province is still set
        frappe.msgprint(f"DEBUG - After Validation: region={self.region}, province={self.province}")
        
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
        if frappe.db.exists("UNEM Member", {
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
            
        # If we have a province, validate it
        if self.province:
            # Ensure province exists
            if not frappe.db.exists("Province", self.province):
                frappe.throw("الإقليم غير موجود")
                
            # Get province document and validate region
            province_doc = frappe.get_doc("Province", self.province)
            
            if province_doc.region != self.region:
                frappe.throw(f"الإقليم المحدد لا ينتمي إلى {self.region}")
                
    def db_insert(self, *args, **kwargs):
        """
        Override db_insert to ensure province is saved correctly
        """
        frappe.msgprint(f"DEBUG - Before Insert: region={self.region}, province={self.province}")
        
        # Ensure we have the province value from validation
        if hasattr(self.flags, 'temp_province'):
            self.province = self.flags.temp_province
            
        return super(UNEMMember, self).db_insert(*args, **kwargs)
        
    def load_from_db(self):
        """
        Override load_from_db to ensure province is loaded correctly
        """
        super(UNEMMember, self).load_from_db()
        
        # Only try to restore province if _doc_before_save exists
        if hasattr(self, '_doc_before_save') and self._doc_before_save:
            if 'province' in self._doc_before_save:
                self.province = self._doc_before_save['province']
            
    def as_dict(self, *args, **kwargs):
        """
        Override as_dict to ensure province is included in the document dictionary
        """
        d = super(UNEMMember, self).as_dict(*args, **kwargs)
        
        # Ensure province is included in the dictionary
        if hasattr(self, 'province'):
            d['province'] = self.province
            
        return d

    def before_insert(self):
        """
        Handle data before first insert.
        """
        frappe.msgprint(f"DEBUG - Before Insert: region={self.region}, province={self.province}")
        
        # Restore province from flags if needed
        if self.region and self.flags.temp_province:
            frappe.msgprint(f"DEBUG - Restoring province from flags: {self.flags.temp_province}")
            self.province = self.flags.temp_province
            
    def before_save(self):
        """
        Handle data changes before saving.
        """
        frappe.msgprint(f"DEBUG - Before Save: region={self.region}, province={self.province}")
        
        # Only clear province if region has changed
        if self.has_value_changed('region'):
            self.province = ''
            self.flags.temp_province = None
            
        # Restore province from flags if needed
        if self.region and self.flags.temp_province:
            frappe.msgprint(f"DEBUG - Restoring province from flags: {self.flags.temp_province}")
            self.province = self.flags.temp_province
            
    def on_update(self):
        """
        Handle after save operations.
        """
        frappe.msgprint(f"DEBUG - On Update: region={self.region}, province={self.province}")
        
        # If province is missing but we have it in flags, set it directly
        if self.region and not self.province and self.flags.temp_province:
            frappe.msgprint(f"DEBUG - Setting province from flags: {self.flags.temp_province}")
            frappe.db.set_value("UNEM Member", self.name, "province", self.flags.temp_province, update_modified=False)
            frappe.db.commit()
            
    def after_insert(self):
        """
        Handle after insert operations.
        """
        frappe.msgprint(f"DEBUG - After Insert: region={self.region}, province={self.province}")
        
        # If province is missing but we have it in flags, set it directly
        if self.region and not self.province and self.flags.temp_province:
            frappe.msgprint(f"DEBUG - Setting province from flags: {self.flags.temp_province}")
            frappe.db.set_value("UNEM Member", self.name, "province", self.flags.temp_province, update_modified=False)
            frappe.db.commit()
