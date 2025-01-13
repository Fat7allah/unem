/**
 * Client-side form controller for UNEM Member DocType.
 * Handles province field validation and filtering based on selected region.
 */
frappe.ui.form.on('UNEM Member', {
    refresh: function(frm) {
        // Set RTL for Arabic interface
        $('body').attr('dir', 'rtl');
        
        // Initialize province field filtering if region exists
        if (frm.doc.region) {
            setup_province_field(frm);
        }
        
        // Log current values
        console.log('Refresh - Current values:', {
            region: frm.doc.region,
            province: frm.doc.province
        });
    },
    
    onload: function(frm) {
        // Initialize province field filtering on form load
        if (frm.doc.region) {
            setup_province_field(frm);
        }
        
        // Log current values
        console.log('Onload - Current values:', {
            region: frm.doc.region,
            province: frm.doc.province
        });
    },
    
    region: function(frm) {
        console.log('Region changed to:', frm.doc.region);
        
        // Reset and reinitialize province when region changes
        frm.set_value('province', '');
        
        if (frm.doc.region) {
            setup_province_field(frm);
        }
    },
    
    before_save: function(frm) {
        console.log('Before Save - Values:', {
            region: frm.doc.region,
            province: frm.doc.province
        });
    },
    
    validate: function(frm) {
        console.log('Validate - Current values:', {
            region: frm.doc.region,
            province: frm.doc.province
        });
        
        // Ensure province is selected if region is set
        if (frm.doc.region && !frm.doc.province) {
            frappe.throw(__('يجب تحديد الإقليم'));
            return false;
        }
        return true;
    },
    
    province: function(frm) {
        console.log('Province changed to:', frm.doc.province);
        
        if (!frm.doc.province) return;
        
        if (!frm.doc.region) {
            frm.set_value('province', '');
            frappe.throw(__('يجب تحديد الجهة أولاً'));
            return;
        }
        
        frappe.db.get_value('Province', frm.doc.province, 'region')
            .then(r => {
                console.log('Province validation result:', r.message);
                if (r.message && r.message.region !== frm.doc.region) {
                    frm.set_value('province', '');
                    frappe.throw(__(`الإقليم المحدد لا ينتمي إلى ${frm.doc.region}`));
                }
            });
    }
});

// Helper function to set up province field
function setup_province_field(frm) {
    console.log('Setting up province field for region:', frm.doc.region);
    frm.set_query('province', function() {
        return {
            filters: {
                'region': frm.doc.region
            }
        };
    });
}
