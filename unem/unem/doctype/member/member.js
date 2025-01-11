// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Member', {
    refresh: function(frm) {
        // Set RTL for Arabic
        $('body').attr('dir', 'rtl');
        
        // Add custom buttons
        frm.add_custom_button(__('إنشاء بطاقة الانخراط'), function() {
            frm.doc.create_membership_card();
            frm.save();
        }, __('إجراءات'));
        
        // Clear province when form loads if no region is selected
        if (!frm.doc.region) {
            frm.set_value('province', '');
        }
    },
    
    validate: function(frm) {
        if (!frm.doc.phone) return;
        
        // Remove any non-digit characters
        let cleanPhone = frm.doc.phone.replace(/\D/g, '');
        
        // Validate phone length
        if (cleanPhone.length < 8 || cleanPhone.length > 15) {
            frappe.throw(__('رقم الهاتف غير صالح'));
        }
        
        frm.set_value('phone', cleanPhone);
    },
    
    profession: function(frm) {
        const teachingProfessions = ['التدريس الابتدائي', 'التدريس الإعدادي', 'التدريس التأهيلي'];
        if (teachingProfessions.includes(frm.doc.profession)) {
            frm.set_df_property('teaching_specialty', 'reqd', 1);
        } else {
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
