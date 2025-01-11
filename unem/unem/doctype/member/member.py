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
        
        # Ensure province is set if region is selected
        if self.region and not self.province:
            frappe.throw("يجب تحديد الإقليم")
            
        # Double-check province exists and belongs to region
        if self.province:
            province_doc = frappe.get_doc("Province", self.province)
            if province_doc.region != self.region:
                self.province = ''
                frappe.throw(f"الإقليم المحدد لا ينتمي إلى {self.region}")

    def on_update(self):
        """Handle after save operations"""
        # Ensure province is saved in the database
        if self.province:
            frappe.db.set_value('Member', self.name, 'province', self.province, update_modified=False)
            frappe.db.commit()

    def before_validate(self):
        """Ensure province is set before validation"""
        if self.region and not self.province:
            frappe.throw("يجب تحديد الإقليم")

    def onload(self):
        """Load province options based on selected region"""
        if self.region:
            provinces = self.get_province_options()
            if provinces:
                self.set_onload('province_options', provinces)

    def get_province_options(self):
        """Get list of provinces for the selected region"""
        provinces_map = {
            'جهة طنجة تطوان الحسيمة': [
                'عمالة طنجة',
                'عمالة تطوان',
                'إقليم الفحص أنجرة',
                'إقليم العرائش',
                'إقليم الحسيمة',
                'إقليم تازة',
                'إقليم شفشاون'
            ],
            'جهة الشرق': [
                'عمالة وجدة أنكاد',
                'إقليم الناظور',
                'إقليم القنيطرة',
                'إقليم تاوريرت',
                'إقليم جرسيف',
                'إقليم بركان',
                'إقليم أوجدا أنكاد'
            ],
            'جهة فاس مكناس': [
                'عمالة فاس',
                'عمالة مكناس',
                'إقليم الحاجب',
                'إقليم إفران',
                'إقليم مولاي يعقوب',
                'إقليم صفرو',
                'إقليم البولمان',
                'إقليم تاونات'
            ],
            'جهة الرباط سلا القنيطرة': [
                'عمالة الرباط',
                'عمالة سلا',
                'عمالة القنيطرة',
                'إقليم الخميسات',
                'إقليم سيدي قاسم',
                'إقليم سیدی سليمان'
            ],
            'جهة بني ملال خنيفرة': [
                'عمالة بني ملال',
                'إقليم خنيفرة',
                'إقليم أزيلال',
                'إقليم الفقيه بن صالح'
            ],
            'جهة الدار البيضاء سطات': [
                'عمالة الدار البيضاء',
                'إقليم المحمدية',
                'إقليم عين السبع الحي المحمدي',
                'إقليم البرنوصي',
                'إقليم مولاي رشيد',
                'إقليم بن مسيك سباتة',
                'إقليم عين الشق',
                'إقليم الفداء',
                'إقليم انفا',
                'إقليم الحي الحسني',
                'إقليم النواصر',
                'إقليم مديونه',
                'اقليم سطات',
                'إقليم الجديدة',
                'إقليم سيدي بنور',
                'إقليم برشيد',
                'إقليم بنسليمان'
            ],
            'جهة مراكش آسفي': [
                'عمالة مراكش',
                'عمالة آسفي',
                'إقليم الحوز',
                'إقليم شيشاوة',
                'إقليم الصويرة',
                'إقليم قلعة السراغنة'
            ],
            'جهة درعة تافيلالت': [
                'إقليم ورزازات',
                'إقليم الراشيدية',
                'إقليم ميدلت',
                'إقليم تينغير'
            ],
            'جهة سوس ماسة': [
                'عمالة أكادير إدا وتنان',
                'عمالة إنزكان آيت ملول',
                'إقليم تارودانت',
                'إقليم تيزنيت',
                'إقليم سيدي إفني'
            ],
            'جهة كلميم واد نون': [
                'إقليم كلميم',
                'إقليم أسا الزاك',
                'إقليم طاطا',
                'إقليم العيون'
            ],
            'جهة العيون الساقية الحمراء': [
                'عمالة العيون',
                'عمالة الساقية الحمراء',
                'إقليم طرفاية'
            ],
            'جهة الداخلة وادي الذهب': [
                'عمالة الداخلة'
            ]
        }
        return provinces_map.get(self.region, [])

@frappe.whitelist()
def get_active_members(doctype, txt, searchfield, start, page_len, filters):
    """Get members with active membership cards"""
    return frappe.db.sql("""
        SELECT DISTINCT m.name, CONCAT(m.first_name, ' ', m.last_name) as full_name
        FROM `tabMember` m
        INNER JOIN `tabMembership_Card` mc ON mc.member = m.name
        WHERE mc.card_status = 'المؤداة'
        AND mc.expiry_date > CURDATE()
        AND (m.name LIKE %(txt)s OR m.first_name LIKE %(txt)s OR m.last_name LIKE %(txt)s)
        ORDER BY m.first_name, m.last_name
        LIMIT %(start)s, %(page_len)s
    """, {
        'txt': f"%{txt}%",
        'start': start,
        'page_len': page_len
    })

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
