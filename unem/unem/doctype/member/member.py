# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Member(Document):
    def validate(self):
        self.validate_email()
        self.validate_phone()
        
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
def get_provinces(doctype, txt, searchfield, start, page_len, filters):
    """Get provinces based on selected region"""
    if not filters.get('region'):
        return []

    return frappe.db.sql("""
        SELECT name, province_name
        FROM `tabProvince`
        WHERE region = %(region)s
        AND (name LIKE %(txt)s OR province_name LIKE %(txt)s)
        ORDER BY province_name ASC
        LIMIT %(start)s, %(page_len)s
    """, {
        'region': filters.get('region'),
        'txt': f"%{txt}%",
        'start': start,
        'page_len': page_len
    })
