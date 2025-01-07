# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, get_first_day, get_last_day

class Expense_Entry(Document):
    """
    Expense Entry document class.
    
    This class represents an expense entry in the system. It contains methods for 
    validating the expense entry data and generating a unique reference number.
    """
    
    def validate(self):
        """
        Validate the expense entry data.
        
        This method calls other validation methods to ensure that the expense entry 
        data is valid.
        """
        self.validate_dates()
        self.validate_amount()
        self.validate_attachments()
        if not self.reference_number:
            self.generate_reference_number()
        
    def validate_dates(self):
        """
        Validate date is within academic year.
        
        This method checks if the date of the expense entry is within the academic 
        year specified.
        """
        if self.date and self.academic_year:
            academic_year = frappe.get_doc("Academic Year", self.academic_year)
            if getdate(self.date) < getdate(academic_year.start_date) or \
               getdate(self.date) > getdate(academic_year.end_date):
                frappe.throw("التاريخ يجب أن يكون ضمن السنة الدراسية المحددة")
                
    def validate_amount(self):
        """
        Validate amount is positive.
        
        This method checks if the amount of the expense entry is positive.
        """
        if self.amount and self.amount <= 0:
            frappe.throw("المبلغ يجب أن يكون أكبر من صفر")
            
    def validate_attachments(self):
        """
        Validate attachments based on amount threshold.
        
        This method checks if attachments are required for the expense entry based 
        on the amount threshold.
        """
        if self.amount > 1000 and not self.attachments:
            frappe.throw("المرفقات مطلوبة للمصاريف التي تتجاوز 1000 درهم")
            
    def generate_reference_number(self):
        """
        Generate unique reference number.
        
        This method generates a unique reference number for the expense entry.
        """
        prefix = "EXP"
        
        fiscal_year = frappe.get_doc("Academic Year", self.academic_year).name
        count = frappe.db.count("Expense_Entry", {
            "academic_year": self.academic_year,
            "category": self.category
        }) + 1
        
        self.reference_number = f"{prefix}-{fiscal_year}-{count:04d}"
        
    def on_submit(self):
        """
        Create GL Entry on submit.
        
        This method creates a General Ledger entry for the expense entry when it 
        is submitted.
        """
        self.create_gl_entry()
        
    def create_gl_entry(self):
        """
        Create General Ledger entry for expense.
        
        This method creates a General Ledger entry for the expense entry.
        """
        # This method will be implemented when GL module is set up
        pass
