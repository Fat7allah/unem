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
        
        // Clear province when form loads if no region is selected
        if (!frm.doc.region) {
            frm.set_value('province', '');
        }
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
    },
    
    region: function(frm) {
        // Clear province when region changes
        frm.set_value('province', '');

        // Set up filters for province field
        frm.set_query('province', function() {
            return {
                filters: {
                    'region': frm.doc.region
                }
            };
        });
    },

    province: function(frm) {
        // Validate that selected province belongs to selected region
        if (frm.doc.province && frm.doc.region) {
            frappe.db.get_value('Province', frm.doc.province, 'region')
                .then(r => {
                    if (r.message && r.message.region !== frm.doc.region) {
                        frm.set_value('province', '');
                        frappe.throw(__(`الإقليم المحدد لا ينتمي إلى ${frm.doc.region}`));
                    }
                });
        }
    }
});

// Helper function to validate email
function validate_email(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
