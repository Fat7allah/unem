import frappe
from frappe.model.document import Document
from frappe.utils import flt

class MembershipCardManagement(Document):
    def validate(self):
        self.validate_province()
        self.calculate_amounts()
        self.validate_payment()
        self.validate_academic_year()
        
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
                
    def calculate_amounts(self):
        """Calculate total amount and shares"""
        # Calculate total amount (100 DH per card)
        self.total_amount = flt(self.card_count * 100)
        
        # Calculate shares
        self.office_share = flt(self.total_amount * 0.5)  # 50%
        self.region_share = flt(self.total_amount * 0.2)  # 20%
        self.province_share = flt(self.total_amount * 0.3)  # 30%
        
        # Calculate remaining balance
        self.remaining_balance = flt(self.payment) - flt(self.total_amount)
        
    def validate_payment(self):
        """Validate payment amount"""
        if not self.payment:
            frappe.throw("يجب تحديد مبلغ الأداء")
            
        if flt(self.payment) < 0:
            frappe.throw("مبلغ الأداء لا يمكن أن يكون سالباً")
            
        if flt(self.card_count) <= 0:
            frappe.throw("عدد البطاقات يجب أن يكون أكبر من 0")
            
        if self.payment and self.payment > self.total_amount:
            frappe.throw("المبلغ المدفوع لا يمكن أن يتجاوز المبلغ الإجمالي")
            
    def validate_academic_year(self):
        if not self.academic_year:
            frappe.throw("يجب تحديد السنة الدراسية")
            
        # Ensure academic year exists
        if not frappe.db.exists("Academic Year", self.academic_year):
            frappe.throw("السنة الدراسية غير موجودة")
            
        # Get membership card
        if self.membership_card:
            card = frappe.get_doc("Membership Card", self.membership_card)
            if card.academic_year != self.academic_year:
                frappe.throw("السنة الدراسية يجب أن تتطابق مع السنة الدراسية في بطاقة الإنخراط")

    def before_save(self):
        """Final calculations before saving"""
        self.calculate_amounts()
        
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
