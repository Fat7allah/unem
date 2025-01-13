/**
 * Client-side form controller for UNEMMember DocType.
 * Handles province field validation and filtering based on selected region.
 */
frappe.ui.form.on('UNEMMember', {
    refresh: function(frm) {
        // Set RTL for Arabic interface
        $('body').attr('dir', 'rtl');
        
        // Initialize province field filtering if region exists
        if (frm.doc.region) {
            setup_province_field(frm);
        }
    },
    
    onload: function(frm) {
        // Initialize province field filtering on form load
        if (frm.doc.region) {
            setup_province_field(frm);
        }
    },
    
    region: function(frm) {
        // Reset and reinitialize province when region changes
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
            query: 'unem.unem.doctype.unem_member.unem_member.get_provinces',
            filters: {
                'region': frm.doc.region
            }
        };
    });
}
