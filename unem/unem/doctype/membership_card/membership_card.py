# Copyright (c) 2025, UNEM and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_years, getdate

class Membership_Card(Document):
    def validate(self):
        self.validate_dates()
        self.validate_card_number()
        
    def validate_dates(self):
        """Validate membership and expiry dates"""
        if self.membership_date and self.expiry_date:
            if getdate(self.expiry_date) <= getdate(self.membership_date):
                frappe.throw("تاريخ الانتهاء يجب أن يكون بعد تاريخ الإنخراط")
                
    def validate_card_number(self):
        """Generate unique card number if not provided"""
        if not self.card_number:
            # Get member details
            member = frappe.get_doc("Member", self.member)
            # Generate card number based on member details
            year = getdate().year
            province_code = self.get_province_code(member.province)
            sequence = frappe.db.count("Membership_Card") + 1
            self.card_number = f"{year}-{province_code}-{sequence:04d}"
            
    def get_province_code(self, province):
        """Get two-letter code for province"""
        province_codes = {
            # Northern Region
            "عمالة طنجة-أصيلة": "TA",
            "عمالة المضيق-الفنيدق": "MF",
            "إقليم تطوان": "TT",
            "إقليم الفحص-أنجرة": "FA",
            "إقليم العرائش": "LA",
            "إقليم الحسيمة": "HS",
            "إقليم شفشاون": "CH",
            "إقليم وزان": "WZ",
            
            # Oriental Region
            "عمالة وجدة-أنجاد": "OJ",
            "إقليم الناظور": "NA",
            "إقليم الدريوش": "DR",
            "إقليم جرادة": "JR",
            "إقليم بركان": "BR",
            "إقليم تاوريرت": "TR",
            "إقليم جرسيف": "GF",
            "إقليم فجيج": "FG",
            
            # Drâa-Tafilalet
            "إقليم الرشيدية": "ER",
            "إقليم ميدلت": "MI",
            "إقليم ورزازات": "WR",
            "إقليم زاكورة": "ZG",
            "إقليم تنغير": "TN",
            
            # Fès-Meknès
            "عمالة فاس": "FS",
            "إقليم مولاي يعقوب": "MY",
            "إقليم صفرو": "SF",
            "إقليم بولمان": "BM",
            "إقليم تاونات": "TA",
            "إقليم تازة": "TZ",
            "عمالة مكناس": "MK",
            "إقليم الحاجب": "EH",
            "إقليم إفران": "IF",
            "إقليم خنيفرة": "KH",
            
            # Rabat-Salé-Kénitra
            "عمالة الرباط": "RB",
            "عمالة سلا": "SL",
            "عمالة الصخيرات-تمارة": "SK",
            "إقليم الخميسات": "KM",
            "إقليم القنيطرة": "KN",
            "إقليم سيدي قاسم": "SQ",
            "إقليم سيدي سليمان": "SS",
            
            # Casablanca-Settat
            "عمالة الدار البيضاء": "CB",
            "عمالة المحمدية": "MH",
            "إقليم النواصر": "NW",
            "إقليم مديونة": "MD",
            "إقليم بنسليمان": "BS",
            "إقليم برشيد": "BE",
            "إقليم سطات": "ST",
            "إقليم الجديدة": "JD",
            "إقليم سيدي بنور": "SB",
            
            # Marrakech-Safi
            "عمالة مراكش": "MR",
            "إقليم شيشاوة": "CH",
            "إقليم الحوز": "EH",
            "إقليم قلعة السراغنة": "KS",
            "إقليم الصويرة": "ES",
            "إقليم الرحامنة": "RH",
            "إقليم آسفي": "AS",
            "إقليم اليوسفية": "YO",
            
            # Souss-Massa
            "إقليم أكادير إدا وتنان": "AU",
            "إقليم إنزكان-آيت ملول": "IN",
            "عمالة أكادير-إداوتنان": "AE",
            "إقليم شتوكة-آيت باها": "CB",
            "إقليم تارودانت": "TR",
            "إقليم تيزنيت": "TZ",
            "إقليم طاطا": "TT",
            
            # Guelmim-Oued Noun
            "إقليم كلميم": "GL",
            "إقليم أسا-الزاك": "AZ",
            "إقليم طانطان": "TN",
            "إقليم سيدي إفني": "SI",
            
            # Laâyoune-Sakia El Hamra
            "إقليم العيون": "LY",
            "إقليم بوجدور": "BJ",
            "إقليم طرفاية": "TR",
            "إقليم السمارة": "SM",
            
            # Dakhla-Oued Ed-Dahab
            "إقليم وادي الذهب": "OD",
            "إقليم أوسرد": "OS"
        }
        return province_codes.get(province, "XX")
        
    def before_save(self):
        """Set expiry date to one year from membership date if not set"""
        if self.membership_date and not self.expiry_date:
            self.expiry_date = add_years(self.membership_date, 1)
