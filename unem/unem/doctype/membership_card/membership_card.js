// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Membership_Card', {
    refresh: function(frm) {
        // Set RTL for Arabic
        $('body').attr('dir', 'rtl');
        
        // Add custom buttons
        if (frm.doc.card_status === "غير المؤداة") {
            frm.add_custom_button(__('تسجيل الدفع'), function() {
                frm.set_value('card_status', 'المؤداة');
                frm.save();
            }, __('إجراءات'));
        }
    },
    
    membership_date: function(frm) {
        // Auto-set expiry date to one year from membership date
        if (frm.doc.membership_date && !frm.doc.expiry_date) {
            let expiry = frappe.datetime.add_years(frm.doc.membership_date, 1);
            frm.set_value('expiry_date', expiry);
        }
    },
    
    validate: function(frm) {
        // Validate dates
        if (frm.doc.membership_date && frm.doc.expiry_date) {
            if (frappe.datetime.str_to_obj(frm.doc.expiry_date) <= 
                frappe.datetime.str_to_obj(frm.doc.membership_date)) {
                frappe.msgprint(__("تاريخ الانتهاء يجب أن يكون بعد تاريخ الإنخراط"));
                frappe.validated = false;
            }
        }
    }
});
