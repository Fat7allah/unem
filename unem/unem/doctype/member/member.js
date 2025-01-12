// Copyright (c) 2025, UNEM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Member', {
    refresh: function(frm) {
        // Set RTL for Arabic
        $('body').attr('dir', 'rtl');
        
        // Set up province field if region exists
        if (frm.doc.region) {
            setup_province_field(frm);
        }
    },
    
    onload: function(frm) {
        // Set up province field on form load if region exists
        if (frm.doc.region) {
            setup_province_field(frm);
        }
    },
    
    region: function(frm) {
        // Clear province when region changes
        frm.set_value('province', '');
        
        if (frm.doc.region) {
            setup_province_field(frm);
        }
    },
    
    province: function(frm) {
        if (!frm.doc.province) return;
        
        if (!frm.doc.region) {
            frm.set_value('province', '');
            frappe.throw(__('يجب تحديد الجهة أولاً'));
            return;
        }
        
        frappe.db.get_value('Province', frm.doc.province, 'region')
            .then(r => {
                if (r.message && r.message.region !== frm.doc.region) {
                    frm.set_value('province', '');
                    frappe.throw(__(`الإقليم المحدد لا ينتمي إلى ${frm.doc.region}`));
                }
            });
    }
});

// Helper function to set up province field
function setup_province_field(frm) {
    frm.set_query('province', function() {
        return {
            filters: {
                'region': frm.doc.region
            }
        };
    });
}
