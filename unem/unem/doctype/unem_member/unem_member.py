# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address

class UNEMMember(Document):
    def validate(self):
        """
        Validate member data before saving.
        Ensures email, phone, and province data are valid.
        """
        frappe.msgprint(f"DEBUG - Validate: region={self.region}, province={self.province}")
        
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
                
    def before_save(self):
        """
        Handle data changes before saving.
        """
        frappe.msgprint(f"DEBUG - Before Save: region={self.region}, province={self.province}")
        
        # Only clear province if region has changed
        if self.has_value_changed('region'):
            self.province = ''
            
        # Store the province value to ensure it's saved
        if self.province:
            # Get the current values from DB if this is an existing document
            if not self.is_new():
                current = frappe.get_doc("UNEM Member", self.name)
                frappe.msgprint(f"DEBUG - Current DB values: region={current.region}, province={current.province}")
            
            # Set the province value explicitly
            frappe.db.set_value("UNEM Member", self.name, "province", self.province, update_modified=False)
            frappe.db.commit()
            frappe.msgprint(f"DEBUG - Explicitly set province to: {self.province}")
            
    def on_update(self):
        """
        Handle after save operations.
        """
        frappe.msgprint(f"DEBUG - On Update: region={self.region}, province={self.province}")
        
        # Double-check the values in the database
        saved_doc = frappe.get_doc("UNEM Member", self.name)
        frappe.msgprint(f"DEBUG - Saved in DB: region={saved_doc.region}, province={saved_doc.province}")
        
        # If province is still missing but we have it in memory, try one more time
        if saved_doc.region and not saved_doc.province and self.province:
            frappe.msgprint("DEBUG - Province still missing, trying one more time")
            frappe.db.set_value("UNEM Member", self.name, "province", self.province, update_modified=False)
            frappe.db.commit()
            
            # Verify the final save
            final_doc = frappe.get_doc("UNEM Member", self.name)
            frappe.msgprint(f"DEBUG - Final DB values: region={final_doc.region}, province={final_doc.province}")
            
    def after_insert(self):
        """
        Handle after insert operations.
        """
        frappe.msgprint(f"DEBUG - After Insert: region={self.region}, province={self.province}")
        
        # Verify the values in the database
        saved_doc = frappe.get_doc("UNEM Member", self.name)
        frappe.msgprint(f"DEBUG - Saved in DB: region={saved_doc.region}, province={saved_doc.province}")
        
        # If province is missing but we have it, set it now
        if saved_doc.region and not saved_doc.province and self.province:
            frappe.msgprint("DEBUG - Setting province after insert")
            frappe.db.set_value("UNEM Member", self.name, "province", self.province, update_modified=False)
            frappe.db.commit()
            
            # Verify the save
            final_doc = frappe.get_doc("UNEM Member", self.name)
            frappe.msgprint(f"DEBUG - Final DB values: region={final_doc.region}, province={final_doc.province}")
