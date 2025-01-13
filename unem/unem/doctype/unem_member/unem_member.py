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
        frappe.logger().debug(f"Validating UNEM Member - Current values: region={self.region}, province={self.province}")
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
        frappe.logger().debug(f"Validating province - Current values: region={self.region}, province={self.province}")
        
        if not self.region:
            return
            
        if not self.province:
            frappe.throw("يجب تحديد الإقليم")
        
        # Ensure province exists
        if not frappe.db.exists("Province", self.province):
            frappe.throw("الإقليم غير موجود")
            
        # Get province document and validate region
        province_doc = frappe.get_doc("Province", self.province)
        frappe.logger().debug(f"Province document loaded: {province_doc.name}, region={province_doc.region}")
        
        if province_doc.region != self.region:
            frappe.throw(f"الإقليم المحدد لا ينتمي إلى {self.region}")
                
    def before_save(self):
        """
        Handle data changes before saving.
        Clears province when region changes.
        """
        frappe.logger().debug(f"Before save - Current values: region={self.region}, province={self.province}")
        if self.has_value_changed('region'):
            frappe.logger().debug("Region changed, clearing province")
            self.province = ''
            
    def on_update(self):
        """
        Log after saving.
        """
        frappe.logger().debug(f"After save - Final values: region={self.region}, province={self.province}")
        
    def after_insert(self):
        """
        Log after insert.
        """
        frappe.logger().debug(f"After insert - Final values: region={self.region}, province={self.province}")
