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
    
    validate: function(frm) {
        // Ensure province is set if region is selected
        if (frm.doc.region && !frm.doc.province) {
            frappe.throw(__('يجب تحديد الإقليم'));
            return false;
        }
        return true;
    },
    
    region: function(frm) {
        // Clear province when region changes
        frm.set_value('province', '');
        
        if (frm.doc.region) {
            setup_province_field(frm);
        }
    },
    
    province: function(frm) {
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

// Helper function to set up province field
function setup_province_field(frm) {
    frm.set_query('province', function() {
        return {
            filters: {
                'region': frm.doc.region
            }
        };
    });
    
    // Fetch provinces for the selected region
    frappe.call({
        method: 'unem.unem.doctype.member.member.get_provinces',
        args: {
            doctype: 'Province',
            txt: '',
            searchfield: 'name',
            start: 0,
            page_len: 50,
            filters: JSON.stringify({ 'region': frm.doc.region })
        },
        callback: function(r) {
            if (!r.exc && r.message && r.message.length > 0) {
                frm.refresh_field('province');
            } else {
                frappe.msgprint(__('لا توجد أقاليم متاحة للجهة المحددة'));
                frm.set_value('region', '');
            }
        }
    });
}

// Helper function to validate email
function validate_email(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
