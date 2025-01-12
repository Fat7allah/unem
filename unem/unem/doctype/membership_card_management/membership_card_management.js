frappe.ui.form.on('membership_card_management', {
    refresh: function(frm) {
        // Set RTL for Arabic
        $('body').attr('dir', 'rtl');
        
        // Set currency to MAD for all currency fields
        frm.set_currency_labels(['total_amount', 'payment', 'remaining_balance', 
            'office_share', 'region_share', 'province_share'], 'MAD');
    },
    
    onload: function(frm) {
        // Set currency to MAD for all currency fields
        frm.set_currency_labels(['total_amount', 'payment', 'remaining_balance', 
            'office_share', 'region_share', 'province_share'], 'MAD');
            
        // Set up province field if region exists
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
    },
    
    card_count: function(frm) {
        calculate_amounts(frm);
    },
    
    payment: function(frm) {
        calculate_amounts(frm);
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

// Helper function to calculate amounts
function calculate_amounts(frm) {
    if (!frm.doc.card_count) {
        frm.doc.card_count = 0;
    }
    
    // Calculate total amount (100 DH per card)
    let total_amount = frm.doc.card_count * 100;
    frm.set_value('total_amount', total_amount);
    
    // Calculate shares
    frm.set_value('office_share', total_amount * 0.5);  // 50%
    frm.set_value('region_share', total_amount * 0.2);  // 20%
    frm.set_value('province_share', total_amount * 0.3); // 30%
    
    // Calculate remaining balance
    if (frm.doc.payment) {
        frm.set_value('remaining_balance', frm.doc.payment - total_amount);
    }
    
    // Set currency to MAD for all currency fields
    frm.set_currency_labels(['total_amount', 'payment', 'remaining_balance', 
        'office_share', 'region_share', 'province_share'], 'MAD');
}
