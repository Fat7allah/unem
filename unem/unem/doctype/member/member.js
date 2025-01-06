// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Member', {
    refresh: function(frm) {
        // Set RTL for Arabic
        $('body').attr('dir', 'rtl');
        
        // Add custom buttons
        frm.add_custom_button(__('إصدار بطاقة العضوية'), function() {
            frm.doc.create_membership_card();
            frm.save();
        }, __('إجراءات'));
    },
    
    validate: function(frm) {
        // Custom client-side validations
        if (frm.doc.email && !validate_email(frm.doc.email)) {
            frappe.msgprint(__('عنوان البريد الإلكتروني غير صالح'));
            frappe.validated = false;
        }
    },
    
    profession: function(frm) {
        // Handle teaching specialty visibility
        const teaching_professions = ['التدريس الابتدائي', 'الإعدادي', 'التأهيلي'];
        if (teaching_professions.includes(frm.doc.profession)) {
            frm.set_df_property('teaching_specialty', 'hidden', 0);
            frm.set_df_property('teaching_specialty', 'reqd', 1);
        } else {
            frm.set_df_property('teaching_specialty', 'hidden', 1);
            frm.set_df_property('teaching_specialty', 'reqd', 0);
            frm.set_value('teaching_specialty', '');
        }
    }
});

// Helper function to validate email
function validate_email(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
