# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, get_first_day, get_last_day

class Income_Entry(Document):
    """
    Document class for Income Entry
    """
    
    def validate(self):
        """
        Validate Income Entry document
        """
        self.validate_dates()
        self.validate_amount()
        if not self.reference_number:
            self.generate_reference_number()
        
    def validate_dates(self):
        """
        Validate date is within academic year
        """
        if self.date and self.academic_year:
            academic_year = frappe.get_doc("Academic Year", self.academic_year)
            if getdate(self.date) < getdate(academic_year.start_date) or \
               getdate(self.date) > getdate(academic_year.end_date):
                frappe.throw("التاريخ يجب أن يكون ضمن السنة الدراسية المحددة")
                
    def validate_amount(self):
        """
        Validate amount is positive
        """
        if self.amount and self.amount <= 0:
            frappe.throw("المبلغ يجب أن يكون أكبر من صفر")
            
    def generate_reference_number(self):
        """
        Generate unique reference number
        """
        if self.type == "بطاقة الإنخراط":
            prefix = "CARD"
        else:
            prefix = "INC"
            
        fiscal_year = frappe.get_doc("Academic Year", self.academic_year).name
        count = frappe.db.count("Income_Entry", {
            "academic_year": self.academic_year,
            "type": self.type
        }) + 1
        
        self.reference_number = f"{prefix}-{fiscal_year}-{count:04d}"
        
    def on_submit(self):
        """
        Create GL Entry on submit
        """
        if self.type == "بطاقة الإنخراط":
            # Update membership card status
            self.update_membership_card()
            
    def update_membership_card(self):
        """
        Update membership card status if payment is for card
        """
        if self.type == "بطاقة الإنخراط" and self.reference_number:
            # Find matching membership card
            membership_card = frappe.get_list("Membership_Card", 
                filters={
                    "member": self.payer_name,
                    "card_status": "غير المؤداة"
                },
                limit=1
            )
            
            if membership_card:
                card = frappe.get_doc("Membership_Card", membership_card[0].name)
                card.card_status = "المؤداة"
                card.payment_reference = self.reference_number
                card.save()
